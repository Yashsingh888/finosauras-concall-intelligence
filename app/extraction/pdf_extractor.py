
import fitz
from pathlib import Path


class PDFExtractor:

    def extract_text(self, pdf_path):

        try:

            pdf_path = Path(pdf_path)

            if not pdf_path.exists():
                print("PDF file not found!")
                return None

            document = fitz.open(pdf_path)

            extracted_text = []

            for page_number, page in enumerate(document, start=1):

                text = page.get_text("text")

                if text.strip():

                    extracted_text.append(
                        f"\n--- Page {page_number} ---\n{text}"
                    )

            document.close()

            final_text = "\n".join(extracted_text)

            print("PDF extraction successful!")
            print("Total characters:", len(final_text))

            return final_text

        except Exception as error:

            print("PDF extraction failed:", error)

            return None


if __name__ == "__main__":

    extractor = PDFExtractor()

    print("PDF Extractor initialized successfully!")
