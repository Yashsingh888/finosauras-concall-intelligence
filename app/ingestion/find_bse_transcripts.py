
import json
from pathlib import Path

from app.ingestion.bse_fetcher import BSEFetcher
from app.ingestion.transcript_filter import TranscriptFilter


def main():

    print("Searching historical BSE transcripts...")

    fetcher = BSEFetcher()

    # Fetch announcements from the last 30 days
    announcements = fetcher.fetch_announcements(days_back=30)

    transcript_filter = TranscriptFilter()

    transcripts = transcript_filter.filter_announcements(
        announcements,
        "BSE"
    )

    # Save all fetched announcements
    output_folder = Path("data/announcements")
    output_folder.mkdir(parents=True, exist_ok=True)

    all_file = output_folder / "bse_announcements.json"

    all_file.write_text(
        json.dumps(announcements, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    # Save only transcript announcements
    transcript_file = output_folder / "bse_transcripts.json"

    transcript_file.write_text(
        json.dumps(transcripts, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\n========== SEARCH RESULTS ==========")
    print("Total announcements:", len(announcements))
    print("Transcript announcements:", len(transcripts))

    for item in transcripts:

        print("\nCompany:", item.get("SLONGNAME"))
        print("Subject:", item.get("NEWSSUB"))
        print("Attachment:", item.get("ATTACHMENTNAME"))
        print("Date:", item.get("DT_TM"))

    print("\nAnnouncement data saved in:", output_folder)


if __name__ == "__main__":
    main()
