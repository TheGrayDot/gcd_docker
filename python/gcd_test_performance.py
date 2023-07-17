import time

from cbdb import gcd_db
from cbdb import gcd_models


# Connect to the GCD database
DB = gcd_db.Database()
DB.connect()


def paginate_issues_test(paginate_limit: int):
    row_count = 20000
    offset = 0
    limit = paginate_limit

    while offset < row_count:
        issues = DB.paginate_all_issues(limit, offset)

        offset += limit

        for issue_dict in issues:
            # Fetch series dict from db
            series_id = str(issue_dict["series_id"])
            series_dict = DB.fetch_series_using_id(series_id)

            # Create new comic object with (my) relevant properties
            comic_dict = dict()
            comic_dict = issue_dict.copy()
            # Remove id from series dict
            series_dict.pop("id")
            # Change name in series dict to series_name
            series_dict["series_name"] = series_dict["name"]
            series_dict.pop("name")
            comic_dict.update(series_dict)


if __name__ == "__main__":
    print("[*] Running...")
    start = time.time()
    paginate_issues_test(100)
    end = time.time()
    elapsed = end - start
    print(f"[*] 100: {elapsed}")

    start = time.time()
    paginate_issues_test(500)
    end = time.time()
    elapsed = end - start
    print(f"[*] 500: {elapsed}")

    start = time.time()
    paginate_issues_test(1000)
    end = time.time()
    elapsed = end - start
    print(f"[*] 1000: {elapsed}")

    start = time.time()
    paginate_issues_test(2000)
    end = time.time()
    elapsed = end - start
    print(f"[*] 2000: {elapsed}")

    start = time.time()
    paginate_issues_test(5000)
    end = time.time()
    elapsed = end - start
    print(f"[*] 5000: {elapsed}")
