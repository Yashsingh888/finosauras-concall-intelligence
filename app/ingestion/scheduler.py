
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from app.ingestion.transcript_collector import TranscriptCollector
from app.database.db import SessionLocal
from app.database.models import Announcement


def collect_and_save_transcripts():

    print("\n========== AUTOMATIC TRANSCRIPT COLLECTION ==========")

    db = SessionLocal()

    try:
        collector = TranscriptCollector()

        transcripts = collector.collect_transcripts()

        new_count = 0
        duplicate_count = 0

        for item in transcripts:

            pdf_url = item.get("pdf_url", "").strip()

            # Skip announcements without a PDF link
            if not pdf_url:
                continue

            # Check whether this PDF already exists
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

        print("\nCollection completed!")
        print("New announcements saved:", new_count)
        print("Duplicate announcements skipped:", duplicate_count)

    except Exception as error:

        db.rollback()
        print("Collection error:", error)

    finally:
        db.close()


scheduler = BackgroundScheduler()


def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(
        collect_and_save_transcripts,
        trigger="interval",
        minutes=30,
        id="transcript_collection_job",
        max_instances=1,
        coalesce=True,
        next_run_time=datetime.now()
    )

    scheduler.start()

    print("Transcript scheduler started!")
    print("Automatic collection interval: 30 minutes")


def stop_scheduler():

    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Transcript scheduler stopped!")
