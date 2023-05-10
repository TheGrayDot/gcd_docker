import datetime

import dateparser
import mysql.connector

from cbdb import gcd_db
from cbdb import comic


TODAY_DT = datetime.datetime.now().strftime("%Y-%m-%d")

DP_SETTINGS = {
    "PREFER_DAY_OF_MONTH": "first",
    "REQUIRE_PARTS": ["year"]
}

# Connect to the GCD database
db = gcd_db.Database()
db.connect()

# Determine issue count
print("[*] Determining row count...")
row_count = 0
query = "SELECT * FROM gcd_issue"
with db.gcd_db.cursor() as cursor:
    cursor.execute(query)
    cursor.fetchall()
    row_count = cursor.rowcount
print(f"[*] row_count: {row_count}")
row_count = 2275369
# row_count = 1000

# Paginate through all issues
print("[*] Starting")
offset = 0
limit = 1000
 
while offset < row_count:
    print(f"[*] offset: {offset}")
    # print(f"[*] row_count: {row_count}")

    issues = db.paginate_all_issues(limit, offset)
    print(f"[*] len(issues): {len(issues)}")

    offset += limit
    issues_updated = list()

    # For each issue in paginated list, update publication date timestamp to object
    for issue_dict in issues:
        issue_id = int(issue_dict["id"])
        print(f"[*] issue_id: {issue_id}")

        # publication_date - convert to datetime
        publication_date = issue_dict["publication_date"]
        publication_dt = dateparser.parse(publication_date, settings=DP_SETTINGS)
        if publication_dt:
            publication_dt = publication_dt.strftime('%Y-%m-%d %H:%M:%S')
            if publication_dt:
                # dateparser returns today's date if not found, set it to None instead
                if publication_dt.startswith(TODAY_DT):
                    publication_dt = None
            issue_dict["publication_date"] = publication_dt
        else:
            issue_dict["publication_date"] = None
        
        # Clean page number property
        number = issue_dict["number"]
        try: 
            number_int = int(number)
        except ValueError:
            number_int = None
        issue_dict["number"] = number_int

        # Create new comic object with (my) relevant properties
        comic_dict = dict()
        series_id = str(issue_dict["series_id"])
        series_dict = db.fetch_series_using_id(series_id)
        publisher_id = str(series_dict["publisher_id"])
        publisher_dict = db.fetch_publisher_using_id(publisher_id)
        comic_dict = comic.populate(issue_dict, series_dict, publisher_dict)
        comic_obj = comic.Comic.parse_obj(comic_dict)

        # Create SQL insert statement
        keys = ", ".join(str(x) for x in comic_dict.keys())
        values = ", ".join(str(x) for x in comic_dict.values())
        qry = f"INSERT INTO tgd_issues ({keys}) VALUES ({values})"
        print(qry)

print("[*] Done")
