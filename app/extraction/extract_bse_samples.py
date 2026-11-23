
import fitz
from pathlib import Path

PDF_FOLDER = Path("data/transcripts")
OUTPUT_FOLDER = Path("data/extracted_text")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

pdf_files = list(PDF_FOLDER.glob("*.pdf"))

if not pdf_files:
    print("No PDF files found!")
else:
    for pdf_path in pdf_files:
        print(f"\nExtracting: {pdf_path.name}")

        try:
            document = fitz.open(pdf_path)
            extracted_text = []

            for page in document:
                extracted_text.append(page.get_text())

            full_text = "\n".join(extracted_text).strip()

            output_name = pdf_path.stem + ".txt"
            output_path = OUTPUT_FOLDER / output_name

            output_path.write_text(
                full_text,
                encoding="utf-8"
            )

            print("Pages:", len(document))
            print("Characters extracted:", len(full_text))
            print("Saved:", output_path)

            if len(full_text) < 100:
                print("WARNING: Very little text extracted. This PDF may need OCR.")

            document.close()

        except Exception as error:
            print("Extraction failed:", error)

    print("\n========== EXTRACTION COMPLETED ==========")
