
from app.ingestion.nse_fetcher import NSEFetcher
from app.ingestion.bse_fetcher import BSEFetcher


def inspect_data(name, announcements):

    print(f"\n========== {name} ==========")

    if not announcements:
        print("No announcements found.")
        return

    print("Total records:", len(announcements))

    # Display the first announcement's field names
    first_record = announcements[0]

    print("\nAvailable fields:")
    for key in first_record.keys():
        print("-", key)

    print("\nFirst announcement:")
    print(first_record)


if __name__ == "__main__":

    nse = NSEFetcher()
    bse = BSEFetcher()

    nse_data = nse.fetch_announcements()
    bse_data = bse.fetch_announcements()

    inspect_data("NSE DATA", nse_data)
    inspect_data("BSE DATA", bse_data)
