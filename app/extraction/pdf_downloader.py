
import requests
from pathlib import Path
import re


class PDFDownloader:

    def __init__(self):

        self.download_folder = Path("data/transcripts")

        self.download_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/pdf,*/*"
        })

    def download_pdf(self, url, company_name):

        try:

            safe_name = re.sub(
                r"[^a-zA-Z0-9_-]",
                "_",
                company_name
            )

            file_path = (
                self.download_folder /
                f"{safe_name}.pdf"
            )

            # Avoid downloading duplicates
            if file_path.exists():
                print("Already downloaded:", file_path)
                return file_path

            response = self.session.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            # Check that response is actually a PDF
            if not response.content.startswith(b"%PDF"):
                print("Downloaded file is not a valid PDF")
                return None

            with open(file_path, "wb") as file:

                file.write(response.content)

            print("PDF downloaded:", file_path)

            return file_path

        except requests.RequestException as error:

            print("Download failed:", error)

            return None


if __name__ == "__main__":

    downloader = PDFDownloader()

    print("PDF Downloader initialized successfully!")

    print("Download folder:", downloader.download_folder)
