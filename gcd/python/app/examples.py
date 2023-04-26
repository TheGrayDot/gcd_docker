import db
import comic


# Connect to the GCD database
gcd_db = db.Database()
gcd_db.connect()

# Lookup a comic using GCD issue ID
issue_id = "41900"
issue = gcd_db.fetch_issue_using_id(issue_id)
print("ISSUE DICTIONARY")
print(issue)

# Find the associated comic series
series_id = str(issue["series_id"])
series = gcd_db.fetch_series_using_id(series_id)
print("SERIES DICTIONARY")
print(series)

# Find the associated comic series
publisher_id = str(series["publisher_id"])
publisher = gcd_db.fetch_publisher_using_id(publisher_id)
print("PUBLISHER DICTIONARY")
print(publisher)

# Use issue/series info to make a comic object
comic_obj = comic.Comic()
comic_obj.populate(issue, series, publisher)
print("COMIC OBJECT")
print(vars(comic_obj))
