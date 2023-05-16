from cbdb import gcd_db
# from cbdb import comic
from cbdb import gcd_models


# Connect to the GCD database
db = gcd_db.Database()
db.connect()

issue_ids = list()
with open("cbdb/example_issue_ids.txt") as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        issue_ids.append(l)

for issue_id in issue_ids:
    # Lookup a comic using GCD issue ID
    comic_dict = dict()
    issue_dict = db.fetch_issue_using_id(issue_id)
    # Find the associated comic series
    series_id = str(issue_dict["series_id"])
    series_dict = db.fetch_series_using_id(series_id)
    # Find the associated comic publisher
    publisher_id = str(series_dict["publisher_id"])
    publisher_dict = db.fetch_publisher_using_id(publisher_id)

    # Create GCD object from GCD data
    gcd_issue = gcd_models.Issue(**issue_dict)
    gcd_series = gcd_models.Series(**series_dict)
    gcd_publisher = gcd_models.Publisher(**publisher_dict)

    # TODO: Finish script to print
