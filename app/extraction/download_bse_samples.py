
import json
import re
from pathlib import Path

import requests


INPUT_FILE = Path("data/announcements/bse_transcripts.json")
OUTPUT_FOLDER = Path("data/transcripts")

BSE_PDF_BASE = (
    "https://www.bseindia.com/xml-data/corpfiling/AttachLive/"
)


def safe_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return re.sub(r"\s+", "_", name).strip("_")


def download_samples():

    if not INPUT_FILE.exists():
        print("Transcript JSON file not found:", INPUT_FILE)
        return

    announcements = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bseindia.com/"
    })

    downloaded = 0
    selected_companies = set()

    for item in announcements:

        subject = str(item.get("NEWSSUB", "")).lower()

        if "transcript" not in subject:
            continue

        company = item.get("SLONGNAME", "Unknown Company")

        if company in selected_companies:
            continue

        attachment = item.get("ATTACHMENTNAME", "")

        if not attachment:
            continue

        if attachment.startswith("http"):
            pdf_url = attachment
        else:
            pdf_url = BSE_PDF_BASE + attachment.lstrip("/")

        filename = safe_filename(company) + ".pdf"
        output_path = OUTPUT_FOLDER / filename

        print("\nDownloading:", company)

        try:
            response = session.get(pdf_url, timeout=45)
            response.raise_for_status()

            content = response.content

            if not content.lstrip().startswith(b"%PDF"):
                print("Invalid PDF response. Skipping:", company)
                continue

            output_path.write_bytes(content)

            print("Saved:", output_path)
            print("Size:", len(content), "bytes")

            selected_companies.add(company)
            downloaded += 1

            if downloaded >= 3:
                break

        except requests.RequestException as error:
            print("Download failed:", error)

    print("\n========== DOWNLOAD RESULTS ==========")
    print("PDFs downloaded:", downloaded)


if __name__ == "__main__":
    download_samples()
