
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.database.db import engine, Base, SessionLocal
from app.database.models import TranscriptSummary


SUMMARY_FOLDER = Path("data/summaries")


def save_summaries():

    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    json_files = list(SUMMARY_FOLDER.glob("*.json"))

    if not json_files:
        print("No JSON summary files found.")
        db.close()
        return

    saved_count = 0

    try:
        for file_path in json_files:

            print("\nReading:", file_path.name)

            with open(file_path, "r", encoding="utf-8") as file:
                summary = json.load(file)

            company_name = summary.get(
                "company",
                file_path.stem.replace("_", " ")
            )

            markdown_path = file_path.with_suffix(".md")

            markdown_text = ""

            if markdown_path.exists():
                markdown_text = markdown_path.read_text(
                    encoding="utf-8"
                )

            # Avoid inserting duplicate company summaries
            existing = db.query(TranscriptSummary).filter_by(
                company_name=company_name,
                transcript_file=file_path.stem
            ).first()

            if existing:
                existing.summary_json = json.dumps(
                    summary,
                    ensure_ascii=False
                )
                existing.summary_markdown = markdown_text

                print("Updated existing record:", company_name)

            else:
                record = TranscriptSummary(
                    company_name=company_name,
                    transcript_file=file_path.stem,
                    summary_json=json.dumps(
                        summary,
                        ensure_ascii=False
                    ),
                    summary_markdown=markdown_text
                )

                db.add(record)
                print("Added:", company_name)

            saved_count += 1

        db.commit()

        print("\n========== DATABASE SAVE COMPLETED ==========")
        print("Summaries processed:", saved_count)

    except Exception as error:
        db.rollback()
        print("Database error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    save_summaries()
