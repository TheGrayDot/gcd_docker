import json

import dateparser
import pandas as pd
import matplotlib.pyplot as plt

import db
import comic


# Connect to the GCD database
gcd_db = db.Database()
gcd_db.connect()

# c = comic.Comic()
# print(vars(c))
# print(vars(c).keys())
# exit(1)

# # Paginate
# running = True
# offset = 0
# while running:

#     pubs = gcd_db.fecth_all_issues_paginate(count=1000, offset=offset)
#     # print(pubs)
#     print(len(pubs))
#     offset=offset+1000

# issues = gcd_db.fecth_all_issues_paginate(count=1000, offset=0)

# Lookup all issues in GCD
issues = gcd_db.fecth_all_issues()
print(len(issues))

# list_issue_dicts = list()

# for issue in issues:
#     series_id = str(issue["series_id"])
#     series = gcd_db.fetch_series_using_id(series_id)
#     publisher_id = str(series["publisher_id"])
#     publisher = gcd_db.fetch_publisher_using_id(publisher_id)
#     # Use issue/series/publisher info to make a comic object
#     comic_obj = comic.Comic()
#     comic_obj.populate(issue, series, publisher)
#     # print(comic_obj.publication_date)
#     # comic_obj.publication_date = dateparser.parse(comic_obj.publication_date)
#     # print(dt)
#     comic_dict = comic_obj.to_json()
#     list_issue_dicts.append(comic_dict)


# https://datascience.stackexchange.com/questions/106462/how-to-plot-the-sum-of-something-over-an-interval-of-time

# df = pd.DataFrame(list_issue_dicts)
# print(df.head())
# print(df.publication_date_ym)
# df.publication_date = pd.to_datetime(df.publication_date)
# print(df.info())
# print(df.publication_date.describe())