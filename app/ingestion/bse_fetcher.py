
import requests
from datetime import datetime, timedelta


class BSEFetcher:

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/155.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.bseindia.com",
            "Referer": "https://www.bseindia.com/"
        })

        self.url = (
            "https://api.bseindia.com/BseIndiaAPI/api/"
            "AnnSubCategoryGetData/w"
        )

    def fetch_announcements(self, days_back=7):

        all_announcements = []

        try:
            for day_offset in range(days_back + 1):

                target_date = datetime.now() - timedelta(
                    days=day_offset
                )

                date_value = target_date.strftime("%Y%m%d")

                print(f"\nFetching BSE date: {date_value}")

                base_params = {
                    "pageno": 1,
                    "strCat": "-1",
                    "strPrevDate": date_value,
                    "strScrip": "",
                    "strSearch": "P",
                    "strToDate": date_value,
                    "strType": "C",
                    "subcategory": "-1"
                }

                response = self.session.get(
                    self.url,
                    params=base_params,
                    timeout=30
                )

                response.raise_for_status()
                data = response.json()

                first_page = data.get("Table", [])
                count_data = data.get("Table1", [])

                if not first_page:
                    print("No announcements for this date.")
                    continue

                total_count = 0

                if count_data:
                    total_count = int(
                        count_data[0].get("ROWCNT", 0)
                    )

                all_announcements.extend(first_page)

                print("Page 1 records:", len(first_page))
                print("Total records reported:", total_count)

                # Fetch remaining pages
                page_size = len(first_page)

                if page_size == 0:
                    continue

                total_pages = (
                    (total_count + page_size - 1) // page_size
                    if total_count else 1
                )

               
                for page in range(2, total_pages + 1):

                    # Create parameters for each page
                    params = base_params.copy()
                    params["pageno"] = page

                    try:
                        page_response = self.session.get(
                            self.url,
                            params=params,
                            timeout=30
                        )

                        page_response.raise_for_status()

                        page_data = page_response.json()
                        records = page_data.get("Table", [])

                        if not records:
                            break

                        all_announcements.extend(records)

                        print(f"Page {page}: {len(records)} records")

                    except requests.RequestException as error:
                        print(f"Page {page} unavailable: {error}")
                        print("Continuing with the next date...")
                        break
        
                    all_announcements.extend(records)
                    print(
                   f"Page {page}: {len(records)} records"
                 )

            # Remove duplicate records
            unique = {}
            for item in all_announcements:
                key = item.get("NEWSID") or item.get("XML_NAME")
                if not key:
                    key = str(item)
                unique[key] = item

            results = list(unique.values())

            print("\nBSE collection completed!")
            print("Total unique announcements:", len(results))

            return results

        except requests.RequestException as error:
            print("BSE request failed:", error)
            return all_announcements

        except (ValueError, KeyError, TypeError) as error:
            print("BSE data processing failed:", error)
            return all_announcements


if __name__ == "__main__":

    fetcher = BSEFetcher()

    announcements = fetcher.fetch_announcements(days_back=7)
