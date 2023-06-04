import json
from datetime import datetime

import dateparser
import mysql.connector

from cbdb import gcd_db
from cbdb import gcd_models
from cbdb import tgd_models


# Datetime object of the last miration
LAST_DUMP_DT = datetime.strptime("1800-05-01 03:41:31", "%Y-%m-%d %H:%M:%S")

# Date parser settings
TODAY_DT = datetime.now().strftime("%Y-%m-%d")
DP_SETTINGS = {
    "PREFER_DAY_OF_MONTH": "first",
    "REQUIRE_PARTS": ["year"]
}

# Published dictionary
with open("cbdb/publishers.json") as f:
    PUBLISHERS = json.load(f)


def has_been_updated(created, modified):
    if created > LAST_DUMP_DT:
        return True
    if modified > LAST_DUMP_DT:
        return True
    return False

# Connect to the GCD database
DB = gcd_db.Database()
DB.connect()

# Determine issue count
# print("[*] Determining row count...")
ROW_COUNT = 0
query = "SELECT * FROM gcd_issue"
with DB.gcd_db.cursor() as cursor:
    cursor.execute(query)
    cursor.fetchall()
    ROW_COUNT = cursor.rowcount
# print(f"[*] ROW_COUNT: {ROW_COUNT}")
# ROW_COUNT = 1000000

# Paginate through all issues
OFFSET = 0
LIMIT = 1000
 
while OFFSET < ROW_COUNT:
    # print(f"[*] OFFSET: {OFFSET}")
    # print(f"[*] ROW_COUNT: {ROW_COUNT}")

    issues = DB.paginate_all_issues(LIMIT, OFFSET)
    # print(f"[*] len(issues): {len(issues)}")

    OFFSET += LIMIT

    for issue_dict in issues:
        # Check last update, and skip if not updated
        created = issue_dict["created"]
        modified = issue_dict["modified"]
        bool_has_been_updated = has_been_updated(created, modified)
        # Skip if issue has not been updated
        if not bool_has_been_updated:
            continue

        # Fetch series dict from db
        series_id = str(issue_dict["series_id"])
        series_dict = DB.fetch_series_using_id(series_id)

        # publication_date - convert to datetime
        publication_date = issue_dict["publication_date"]
        publication_dt = dateparser.parse(publication_date, settings=DP_SETTINGS)
        if publication_dt:
            publication_dt = publication_dt.strftime('%Y-%m-%d %H:%M:%S')
            if publication_dt:
                # dateparser returns today's date if not found
                # So set it to None instead
                if publication_dt.startswith(TODAY_DT):
                    publication_dt = None
            issue_dict["publication_date"] = publication_dt
        else:
            issue_dict["publication_date"] = None

        # Create new comic object with (my) relevant properties
        comic_dict = dict()
        comic_dict = issue_dict.copy()
        # Remove id from series dict
        series_dict.pop("id")
        # Change name in series dict to series_name
        series_dict["series_name"] = series_dict["name"]
        series_dict.pop("name")
        comic_dict.update(series_dict)
        # Fetch publisher name from JSON file
        publisher_id = str(series_dict["publisher_id"])
        comic_dict["publisher_name"] = PUBLISHERS[publisher_id]

        # Make a TGD comic object
        tgd_comic = tgd_models.Comic(**comic_dict)

        # Create SQL insert statement
        keys = ", ".join(str(x) for x in comic_dict.keys())
        values = ", ".join(str(x) for x in comic_dict.values())
        qry = f"INSERT INTO tgd_issues ({keys}) VALUES ({values})"
        print(qry)

# print("[*] Done")
