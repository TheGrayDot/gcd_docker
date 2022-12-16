import db
import comic


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
    issue_dict = gcd_db.fetch_issue_dict_using_id(issue_id)
    # Find the associated comic series
    series_id = str(issue_dict["series_id"])
    series_dict = gcd_db.fetch_series_dict_using_id(series_id)
    # Find the associated comic publisher
    publisher_id = str(series_dict["publisher_id"])
    publisher_dict = gcd_db.fetch_publisher_dict_using_id(publisher_id)
    # Use issue/series info to make a comic object
    comic_obj = comic.Comic()
    comic_obj.populate(issue_dict, series_dict, publisher_dict)
    # comic_obj.print_for_spreadsheet()
    comic_obj.print_gcd_style_title()
