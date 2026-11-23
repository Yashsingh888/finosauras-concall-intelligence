
import json
from pathlib import Path

from app.summarization.ai_summarizer import AISummarizer
from app.summarization.summary_formatter import SummaryFormatter

from app.database.db import Base, engine, SessionLocal
from app.database.models import TranscriptSummary


INPUT_FOLDER = Path("data/extracted_text")


def save_to_database(summary, company_name, transcript_file, markdown_path):

    db = SessionLocal()

    try:
        existing = db.query(TranscriptSummary).filter_by(
            transcript_file=transcript_file
        ).first()

        summary_json = json.dumps(
            summary,
            indent=4,
            ensure_ascii=False
        )

        markdown_text = markdown_path.read_text(encoding="utf-8")

        if existing:
            existing.company_name = company_name
            existing.summary_json = summary_json
            existing.summary_markdown = markdown_text
        else:
            record = TranscriptSummary(
                company_name=company_name,
                transcript_file=transcript_file,
                summary_json=summary_json,
                summary_markdown=markdown_text
            )
            db.add(record)

        db.commit()
        return True

    except Exception as error:
        db.rollback()
        print("Database save failed:", error)
        raise

    finally:
        db.close()


def main():

    print("\n========== FINOSAURAS AI PIPELINE ==========")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        text_files = sorted(INPUT_FOLDER.glob("*.txt"))

        processed_files = {
            record.transcript_file
            for record in db.query(TranscriptSummary.transcript_file).all()
        }

        new_files = [
            file_path for file_path in text_files
            if file_path.stem not in processed_files
        ]

    finally:
        db.close()

    if not new_files:
        print("No new transcripts available for summarization.")
        return

    print("New transcripts found:", len(new_files))

    summarizer = AISummarizer()
    formatter = SummaryFormatter()

    successful_count = 0
    failed_count = 0

    for file_path in new_files:

        print("\nProcessing:", file_path.name)

        try:
            transcript_text = file_path.read_text(encoding="utf-8")

            if len(transcript_text.strip()) < 100:
                print("Transcript is too short. Skipping.")
                failed_count += 1
                continue

            summary = summarizer.summarize(transcript_text)

            company_name = file_path.stem.replace("_", " ")

            if not summary.get("company") or str(
                summary.get("company")
            ).strip().lower() in ["not mentioned", "unknown", "none"]:

                summary["company"] = company_name

            formatter.save_json(summary, company_name)
            formatter.save_markdown(summary, company_name)

            markdown_path = (
                Path("data/summaries")
                / f"{company_name.replace(' ', '_')}.md"
            )

            save_to_database(
                summary,
                company_name,
                file_path.stem,
                markdown_path
            )

            successful_count += 1

            print("Summary saved successfully:", company_name)

        except Exception as error:
            failed_count += 1
            print("Processing failed:", error)

    print("\n========== PIPELINE FINISHED ==========")
    print("Successful:", successful_count)
    print("Failed:", failed_count)


if __name__ == "__main__":
    main()
