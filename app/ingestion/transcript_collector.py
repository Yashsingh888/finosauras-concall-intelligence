
from app.ingestion.nse_fetcher import NSEFetcher
from app.ingestion.bse_fetcher import BSEFetcher
from app.ingestion.transcript_filter import TranscriptFilter


class TranscriptCollector:

    def __init__(self):

        self.nse = NSEFetcher()
        self.bse = BSEFetcher()
        self.filter = TranscriptFilter()

    def collect_transcripts(self):

        print("Fetching NSE announcements...")

        nse_data = self.nse.fetch_announcements()

        print("Fetching BSE announcements...")

        bse_data = self.bse.fetch_announcements()

        nse_transcripts = self.filter.filter_announcements(
            nse_data, "NSE"
        )

        bse_transcripts = self.filter.filter_announcements(
            bse_data, "BSE"
        )

        results = []

        for item in nse_transcripts:

            results.append({
                "exchange": "NSE",
                "company": item.get("sm_name", ""),
                "subject": item.get("attchmntText", ""),
                "pdf_url": item.get("attchmntFile", ""),
                "date": item.get("an_dt", ""),
                "symbol": item.get("symbol", "")
            })

        for item in bse_transcripts:

            attachment = item.get("ATTACHMENTNAME", "")

            pdf_url = ""

            if attachment.startswith("http"):
                pdf_url = attachment
            elif attachment:
                pdf_url = (
                    "https://www.bseindia.com/xml-data/corpfiling/AttachLive/"
                    + attachment
                )

            results.append({
                "exchange": "BSE",
                "company": item.get("SLONGNAME", ""),
                "subject": item.get("NEWSSUB", ""),
                "pdf_url": pdf_url,
                "date": item.get("DT_TM", ""),
                "symbol": item.get("SCRIP_CD", "")
            })

        print("\nTotal transcript announcements:", len(results))

        return results


if __name__ == "__main__":

    collector = TranscriptCollector()

    transcripts = collector.collect_transcripts()

    for transcript in transcripts:

        print("\n------------------------")
        print("Company:", transcript["company"])
        print("Exchange:", transcript["exchange"])
        print("Subject:", transcript["subject"])
        print("PDF:", transcript["pdf_url"])
