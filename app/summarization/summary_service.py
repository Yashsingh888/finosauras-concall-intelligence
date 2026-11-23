
import json
import hashlib

from app.summarization.ai_summarizer import AISummarizer
from app.summarization.summary_formatter import SummaryFormatter

from app.database.db import SessionLocal
from app.database.models import TranscriptSummary


class SummaryService:

    def __init__(self):
        self.summarizer = AISummarizer()
        self.formatter = SummaryFormatter()

    def generate_summary(
        self,
        transcript_text,
        company_name,
        transcript_id=None
    ):

        if not transcript_text or not transcript_text.strip():
            raise ValueError("Transcript text is empty.")

        # Generate a stable ID if one is not provided
        if not transcript_id:
            transcript_id = hashlib.sha256(
                transcript_text.encode("utf-8")
            ).hexdigest()[:12]

        print(f"Generating summary for {company_name}...")

        # 1. Generate AI summary
        summary = self.summarizer.summarize(transcript_text)

        # Use the supplied company name if Gemini doesn't provide one
        if not summary.get("company"):
            summary["company"] = company_name

        # 2. Save JSON
        json_path = self.formatter.save_json(
            summary,
            company_name,
            transcript_id
        )

        # 3. Save Markdown
        markdown_path = self.formatter.save_markdown(
            summary,
            company_name,
            transcript_id
        )

        # 4. Save summary in SQLite
        db = SessionLocal()

        try:
            existing = db.query(TranscriptSummary).filter_by(
                transcript_file=transcript_id
            ).first()

            summary_json = json.dumps(
                summary,
                ensure_ascii=False,
                indent=4
            )

            markdown_text = markdown_path.read_text(
                encoding="utf-8"
            )

            if existing:
                existing.company_name = company_name
                existing.summary_json = summary_json
                existing.summary_markdown = markdown_text

            else:
                record = TranscriptSummary(
                    company_name=company_name,
                    transcript_file=transcript_id,
                    summary_json=summary_json,
                    summary_markdown=markdown_text
                )

                db.add(record)

            db.commit()

            print("Summary saved successfully in SQLite!")

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        return summary
