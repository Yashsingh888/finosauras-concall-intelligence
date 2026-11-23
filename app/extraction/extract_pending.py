
from pathlib import Path

from app.database.db import SessionLocal
from app.database.models import Announcement
from app.extraction.pdf_extractor import PDFExtractor


def extract_pending_transcripts():

    print("\n========== PDF TEXT EXTRACTION ==========")

    db = SessionLocal()
    extractor = PDFExtractor()

    pdf_folder = Path("data/transcripts")
    text_folder = Path("data/extracted_text")

    text_folder.mkdir(parents=True, exist_ok=True)

    extracted_count = 0
    failed_count = 0

    try:
        announcements = db.query(Announcement).filter_by(
            status="downloaded"
        ).all()

        print("PDFs waiting for extraction:", len(announcements))

        for announcement in announcements:

            print("\nProcessing:", announcement.company_name)

            safe_name = "".join(
                ch if ch.isalnum() or ch in "_-" else "_"
                for ch in announcement.company_name
            )

            pdf_path = pdf_folder / f"{safe_name}.pdf"
            text_path = text_folder / f"{safe_name}.txt"

            if not pdf_path.exists():
                print("PDF file not found:", pdf_path)
                announcement.status = "failed"
                failed_count += 1
                db.commit()
                continue

            if text_path.exists() and text_path.stat().st_size > 100:
                print("Text already extracted:", text_path)
                announcement.status = "extracted"
                extracted_count += 1
                db.commit()
                continue

            text = extractor.extract_text(pdf_path)

            if text and len(text.strip()) > 100:
                text_path.write_text(text, encoding="utf-8")
                announcement.status = "extracted"
                extracted_count += 1
                print("Text saved:", text_path)
            else:
                announcement.status = "extraction_failed"
                failed_count += 1

            db.commit()

        print("\n========== EXTRACTION RESULTS ==========")
        print("Successfully extracted:", extracted_count)
        print("Failed extractions:", failed_count)

    except Exception as error:
        db.rollback()
        print("Extraction error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    extract_pending_transcripts()
