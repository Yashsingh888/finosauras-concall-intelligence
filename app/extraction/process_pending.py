
from app.database.db import SessionLocal
from app.database.models import Announcement
from app.extraction.pdf_downloader import PDFDownloader


def download_pending_transcripts():

    print("\n========== DOWNLOADING PENDING TRANSCRIPTS ==========")

    db = SessionLocal()
    downloader = PDFDownloader()

    downloaded_count = 0
    failed_count = 0

    try:
        pending_announcements = db.query(Announcement).filter_by(
            status="pending"
        ).all()

        print("Pending announcements:", len(pending_announcements))

        for announcement in pending_announcements:

            print("\nProcessing:", announcement.company_name)

            file_path = downloader.download_pdf(
                announcement.pdf_url,
                announcement.company_name
            )

            if file_path:
                announcement.status = "downloaded"
                downloaded_count += 1
            else:
                announcement.status = "failed"
                failed_count += 1

            db.commit()

        print("\n========== DOWNLOAD RESULTS ==========")
        print("Successfully downloaded:", downloaded_count)
        print("Failed downloads:", failed_count)

    except Exception as error:
        db.rollback()
        print("Processing error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    download_pending_transcripts()
