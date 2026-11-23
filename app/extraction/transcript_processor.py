
import hashlib
import re
from pathlib import Path

from app.extraction.pdf_downloader import PDFDownloader
from app.extraction.pdf_extractor import PDFExtractor
from app.summarization.summary_service import SummaryService


class TranscriptProcessor:

    def __init__(self):
        self.downloader = PDFDownloader()
        self.extractor = PDFExtractor()
        self.summary_service = SummaryService()

    def process_and_summarize(self, pdf_url, company_name):

        print(f"\nProcessing transcript: {company_name}")

        # Generate the same ID used by PDFDownloader
        transcript_id = hashlib.sha256(
            pdf_url.encode("utf-8")
        ).hexdigest()[:12]

        # Step 1: Download PDF
        pdf_path = self.downloader.download_pdf(
            pdf_url,
            company_name
        )

        if not pdf_path:
            raise Exception("PDF download failed")

        # Step 2: Extract PDF text
        extracted_text = self.extractor.extract_text(pdf_path)

        if not extracted_text or len(extracted_text.strip()) < 100:
            raise Exception("Transcript text is empty or too short")

        # Step 3: Save extracted text
        output_folder = Path("data/extracted_text")
        output_folder.mkdir(parents=True, exist_ok=True)

        safe_name = re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            company_name
        )

        text_path = output_folder / (
            f"{safe_name}_{transcript_id}.txt"
        )

        text_path.write_text(
            extracted_text,
            encoding="utf-8"
        )

        print("Extracted text saved:", text_path)

        # Step 4: Generate summary and save JSON,
        # Markdown and SQLite using the same ID
        summary = self.summary_service.generate_summary(
            extracted_text,
            company_name,
            transcript_id=transcript_id
        )

        print("Complete transcript processing successful!")

        return summary


if __name__ == "__main__":

    processor = TranscriptProcessor()

    print("Transcript Processor initialized successfully!")
