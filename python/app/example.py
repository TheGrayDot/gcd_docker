import db
import comic


# Connect to the GCD database
gcd_db = db.Database()
gcd_db.connect()

# Lookup a comic using GCD issue ID
issue_id = "41900"
issue_dict = gcd_db.fetch_issue_dict_using_id(issue_id)
print("ISSUE DICTIONARY")
print(issue_dict)

# Find the associated comic series
series_id = str(issue_dict["series_id"])
series_dict = gcd_db.fetch_series_dict_using_id(series_id)
print("SERIES DICTIONARY")
print(series_dict)

# Find the associated comic series
publisher_id = str(series_dict["publisher_id"])
publisher_dict = gcd_db.fetch_publisher_dict_using_id(publisher_id)
print("PUBLISHER DICTIONARY")
print(publisher_dict)

# Use issue/series info to make a comic object
comic_obj = comic.Comic()
comic_obj.populate(issue_dict, series_dict, publisher_dict)
print("COMIC OBJECT")
print(vars(comic_obj))
