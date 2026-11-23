
import requests
from datetime import datetime, timedelta


class NSEFetcher:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/"
        })

        self.home_url = "https://www.nseindia.com/companies-listing/corporate-filings-announcements"

        self.api_url = "https://www.nseindia.com/api/corporate-announcements"

    def fetch_announcements(self):

        try:

            # First visit NSE website to establish session
            self.session.get(
                self.home_url,
                timeout=30
            )

            today = datetime.now()
            start_date = today - timedelta(days=30)

            params = {
                "index": "equities",
                "from_date": start_date.strftime("%d-%m-%Y"),
                "to_date": today.strftime("%d-%m-%Y")
            }

            response = self.session.get(
                self.api_url,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            print("NSE connection successful!")
            print("Total announcements:", len(data))

            return data

        except requests.RequestException as error:

            print("NSE request failed:", error)
            return []

        except ValueError as error:

            print("NSE JSON parsing failed:", error)
            return []


if __name__ == "__main__":

    fetcher = NSEFetcher()

    announcements = fetcher.fetch_announcements()
