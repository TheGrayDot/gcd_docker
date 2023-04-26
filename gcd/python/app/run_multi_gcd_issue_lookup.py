import db
from model import comic


# Connect to the GCD database
gcd_db = db.Database()
gcd_db.connect()

issue_ids = list()
with open("example_issue_ids.txt") as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        issue_ids.append(l)

for issue_id in issue_ids:
    # Lookup a comic using GCD issue ID
    comic_dict = dict()
    issue_dict = gcd_db.fetch_issue_using_id(issue_id)
    # Find the associated comic series
    series_id = str(issue_dict["series_id"])
    series_dict = gcd_db.fetch_series_using_id(series_id)
    # Find the associated comic publisher
    publisher_id = str(series_dict["publisher_id"])
    publisher_dict = gcd_db.fetch_publisher_using_id(publisher_id)

    # Create Comic object from GCD data
    comic_dict = comic.create_comic_dict_from_gcd_data(issue_dict, series_dict, publisher_dict)
    comic_obj = comic.Comic.parse_obj(comic_dict)
    comic_obj.print_gcd_style_title()
