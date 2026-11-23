
import asyncio
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.ingestion.transcript_collector import TranscriptCollector
from app.database.db import SessionLocal
from app.database.models import Announcement
from app.api.notifications import send_notification


# FastAPI's event loop, used for WebSocket notifications
server_loop = None


def notify_dashboard(event_type, company_name, message):

    if server_loop is None or server_loop.is_closed():
        print("WebSocket notification skipped: server loop unavailable")
        return

    try:
        future = asyncio.run_coroutine_threadsafe(
            send_notification(event_type, company_name, message),
            server_loop
        )

        def handle_result(result):
            try:
                result.result()
            except Exception as error:
                print("Notification error:", error)

        future.add_done_callback(handle_result)

    except Exception as error:
        print("Could not schedule notification:", error)


def collect_and_save_transcripts():

    print("\n========== TRANSCRIPT COLLECTION ==========")

    db = SessionLocal()

    try:
        collector = TranscriptCollector()
        transcripts = collector.collect_transcripts()

        new_count = 0
        duplicate_count = 0

        for item in transcripts:

            pdf_url = (item.get("pdf_url") or "").strip()

            if not pdf_url:
                continue

            existing = db.query(Announcement).filter_by(
                pdf_url=pdf_url
            ).first()

            if existing:
                duplicate_count += 1
                continue

            announcement = Announcement(
                company_name=item.get("company", "Unknown"),
                exchange=item.get("exchange", ""),
                subject=item.get("subject", ""),
                pdf_url=pdf_url,
                status="pending"
            )

            db.add(announcement)
            new_count += 1

        db.commit()

        print("New announcements:", new_count)
        print("Duplicates skipped:", duplicate_count)

        return new_count

    except Exception as error:
        db.rollback()
        print("Collection error:", error)
        return 0

    finally:
        db.close()


def process_pending_transcripts():

    print("\n========== PROCESSING PENDING TRANSCRIPTS ==========")

    # Import here to avoid unnecessary initialization
    # when the application starts.
    from app.extraction.transcript_processor import TranscriptProcessor

    db = SessionLocal()

    try:
        pending = db.query(Announcement).filter_by(
            status="pending"
        ).all()

        # Copy the required data before closing the session
        announcements = [
            {
                "id": item.id,
                "company_name": item.company_name,
                "pdf_url": item.pdf_url
            }
            for item in pending
        ]

    finally:
        db.close()

    print("Pending announcements:", len(announcements))

    processor = TranscriptProcessor()

    for item in announcements:

        announcement_id = item["id"]
        company_name = item["company_name"]
        pdf_url = item["pdf_url"]

        # Mark as processing before starting
        db = SessionLocal()

        try:
            record = db.query(Announcement).filter_by(
                id=announcement_id
            ).first()

            if not record or record.status != "pending":
                continue

            record.status = "processing"
            db.commit()

        finally:
            db.close()

        try:
            print("\nProcessing:", company_name)

            processor.process_and_summarize(
                pdf_url,
                company_name
            )

            db = SessionLocal()

            try:
                record = db.query(Announcement).filter_by(
                    id=announcement_id
                ).first()

                if record:
                    record.status = "completed"
                    db.commit()

            finally:
                db.close()

            notify_dashboard(
                "transcript_completed",
                company_name,
                "Transcript summary generated successfully."
            )

            print("Processing completed:", company_name)

        except Exception as error:

            print("Processing failed:", company_name, error)

            db = SessionLocal()

            try:
                record = db.query(Announcement).filter_by(
                    id=announcement_id
                ).first()

                if record:
                    record.status = "failed"
                    db.commit()

            finally:
                db.close()

            notify_dashboard(
                "transcript_failed",
                company_name,
                f"Transcript processing failed: {error}"
            )


def run_pipeline_cycle():

    print("\n========== AUTOMATIC PIPELINE CYCLE ==========")

    collect_and_save_transcripts()
    process_pending_transcripts()

    print("\n========== PIPELINE CYCLE FINISHED ==========")


scheduler = BackgroundScheduler()


def start_scheduler():

    global server_loop

    if scheduler.running:
        return

    try:
        server_loop = asyncio.get_running_loop()
    except RuntimeError:
        server_loop = None

    scheduler.add_job(
        run_pipeline_cycle,
        trigger="interval",
        minutes=30,
        id="complete_transcript_pipeline",
        max_instances=1,
        coalesce=True,
        next_run_time=datetime.now()
    )

    scheduler.start()

    print("Automatic transcript pipeline started!")
    print("Collection and processing interval: 30 minutes")


def stop_scheduler():

    global server_loop

    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Automatic transcript pipeline stopped!")

    server_loop = None
