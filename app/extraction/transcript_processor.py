
from app.extraction.pdf_downloader import PDFDownloader
from app.extraction.pdf_extractor import PDFExtractor
from pathlib import Path


class TranscriptProcessor:

    def __init__(self):

        self.downloader = PDFDownloader()
        self.extractor = PDFExtractor()

    def process_transcript(self, pdf_url, company_name):

        print(f"\nProcessing transcript: {company_name}")

        # Step 1: Download PDF
        pdf_path = self.downloader.download_pdf(
            pdf_url,
            company_name
        )

        if not pdf_path:
            print("PDF download failed!")
            return None

        # Step 2: Extract PDF text
        extracted_text = self.extractor.extract_text(
            pdf_path
        )

        if not extracted_text or not extracted_text.strip():

            print("No readable text found in PDF!")
            return None

        # Step 3: Save extracted text
        output_folder = Path("data/extracted_text")

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_path = output_folder / (
            Path(pdf_path).stem + ".txt"
        )

        output_path.write_text(
            extracted_text,
            encoding="utf-8"
        )

        print("\nTranscript processing completed!")
        print("Extracted text saved at:", output_path)

        return extracted_text


if __name__ == "__main__":

    processor = TranscriptProcessor()

    print("Transcript Processor initialized successfully!")
