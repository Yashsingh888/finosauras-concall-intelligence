
from pathlib import Path

from app.summarization.summary_service import SummaryService


def run_pipeline():

    # Location of extracted transcript text
    input_folder = Path("data/extracted_text")

    # Find transcript text files
    transcript_files = list(input_folder.glob("*.txt"))

    if not transcript_files:
        print("No extracted transcript files found.")
        print("Please add a .txt file inside data/extracted_text/")
        return

    # Initialize summary service
    summary_service = SummaryService()

    # Process each transcript
    for file_path in transcript_files:

        print("\n================================")
        print("Processing:", file_path.name)
        print("================================")

        transcript_text = file_path.read_text(
            encoding="utf-8"
        )

        company_name = file_path.stem

        try:
            summary_service.generate_summary(
                transcript_text,
                company_name
            )

            print("Completed:", company_name)

        except Exception as error:
            print("Failed:", company_name)
            print("Reason:", error)

if __name__ == "__main__":
    run_pipeline()
