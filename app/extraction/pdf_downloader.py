import requests
from pathlib import Path
import re
import hashlib


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

            # Generate a unique ID from the PDF URL
            url_hash = hashlib.sha256(
                url.encode("utf-8")
            ).hexdigest()[:12]

            file_path = (
                self.download_folder /
                f"{safe_name}_{url_hash}.pdf"
            )

            # Reuse only the matching transcript
            if file_path.exists():
                print("Already downloaded:", file_path)
                return file_path

            response = self.session.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            if not response.content.startswith(b"%PDF"):
                print("Downloaded file is not a valid PDF")
                return None

            file_path.write_bytes(response.content)

            print("PDF downloaded:", file_path)

            return file_path

        except requests.RequestException as error:

            print("Download failed:", error)
            return None

        except Exception as error:

            print("Unexpected download error:", error)
            return None


if __name__ == "__main__":

    downloader = PDFDownloader()

    print("PDF Downloader initialized successfully!")