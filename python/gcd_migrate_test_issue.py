import os
import json
from datetime import datetime

import dateparser
import mysql.connector

from cbdb import gcd_db
from cbdb import tgd_models


GCD_DUMP_DATE_LAST = os.environ.get("GCD_DUMP_DATE_LAST")
GCD_DUMP_DATE_CURR = os.environ.get("GCD_DUMP_DATE_CURR")

# Date parser settings
TODAY_DT = datetime.now().strftime("%Y-%m-%d")
EARLIEST_DT = datetime.strptime("1901-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
DP_SETTINGS = {"PREFER_DAY_OF_MONTH": "first", "REQUIRE_PARTS": ["year"]}

# Published dictionary
with open(f"cbdb/publishers_{GCD_DUMP_DATE_CURR}.json") as f:
    PUBLISHERS = json.load(f)

# Connect to the GCD database
DB = gcd_db.Database()
DB.connect()

# Select specific issue ID to test
test_issue_id = 1437272

issue_dict = DB.fetch_issue_using_id(test_issue_id)

# Fetch series dict from db
series_id = str(issue_dict["series_id"])
series_dict = DB.fetch_series_using_id(series_id)

# publication_date - convert to datetime
publication_date = issue_dict["publication_date"]
publication_dt = dateparser.parse(publication_date, settings=DP_SETTINGS)
if publication_dt:
    if publication_dt < EARLIEST_DT:
        publication_dt = None
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

tgd_comic = tgd_models.Comic(**comic_dict)
