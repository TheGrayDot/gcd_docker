import json
from datetime import datetime

import pydantic
import dateparser
import mysql.connector

from cbdb import gcd_db
from cbdb import tgd_models


# Date parser settings
TODAY_DT = datetime.now().strftime("%Y-%m-%d")
DP_SETTINGS = {
    "PREFER_DAY_OF_MONTH": "first",
    "REQUIRE_PARTS": ["year"]
}

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
        try:
            tgd_comic = tgd_models.Comic(**comic_dict)
        except pydantic.error_wrappers.ValidationError:
            print(f"Error: OFFSET = {OFFSET}")
            print(f"Error: issue_id = {issue_dict['id']}")
            continue

        # Create SQL insert statement
        keys = ", ".join(str(x) for x in comic_dict.keys())
        values = ", ".join(str(x) for x in comic_dict.values())
        qry = f"INSERT INTO tgd_issues ({keys}) VALUES ({values})"
        print(qry)
