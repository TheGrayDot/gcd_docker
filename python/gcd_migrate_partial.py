import json
from datetime import datetime

import dateparser
import mysql.connector

from cbdb import gcd_db
from cbdb import tgd_models


# Datetime object of the last miration
LAST_DUMP_DT = datetime.strptime("2023-06-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# Date parser settings
TODAY_DT = datetime.now().strftime("%Y-%m-%d")
DP_SETTINGS = {"PREFER_DAY_OF_MONTH": "first", "REQUIRE_PARTS": ["year"]}

# Published dictionary
with open("cbdb/publishers.json") as f:
    PUBLISHERS = json.load(f)

# Connect to the GCD database
DB = gcd_db.Database()
DB.connect()

# Determine issue count
ROW_COUNT = 0
query = "SELECT * FROM gcd_issue"
with DB.gcd_db.cursor() as cursor:
    cursor.execute(query)
    cursor.fetchall()
    ROW_COUNT = cursor.rowcount

# Paginate through all issues
OFFSET = 0
LIMIT = 1000

while OFFSET < ROW_COUNT:
    issues = DB.paginate_all_issues(LIMIT, OFFSET)
    OFFSET += LIMIT

    for issue_dict in issues:
        # Check if issue has been created or updated
        created = issue_dict["created"]
        created_date = created.strftime("%Y-%m-%d %H:%M:%S")
        modified = issue_dict["modified"]
        modified_date = modified.strftime("%Y-%m-%d %H:%M:%S")

        # If not created/modified since last dump
        # Continue to next result
        if created_date < LAST_DUMP_DT:
            continue
        if modified_date < LAST_DUMP_DT:
            continue

        # Fetch series dict from db
        series_id = str(issue_dict["series_id"])
        series_dict = DB.fetch_series_using_id(series_id)

        # publication_date - convert to datetime
        publication_date = issue_dict["publication_date"]
        publication_dt = dateparser.parse(publication_date, settings=DP_SETTINGS)
        if publication_dt:
            publication_dt = publication_dt.strftime("%Y-%m-%d %H:%M:%S")
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

        # If issue created, make insert statement
        if created_date < LAST_DUMP_DT:
            qry = f"INSERT INTO tgd_issues ({keys}) VALUES ({values})"
            print(qry)
        # If issue has been modified, delete then update
        else:
            qry = f"DELETE tgd_issues WHERE id = {issue_dict['id']}"
            print(qry)
            qry = f"INSERT INTO tgd_issues ({keys}) VALUES ({values})"
            print(qry)
