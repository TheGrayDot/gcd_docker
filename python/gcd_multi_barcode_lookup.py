from cbdb import gcd_db
from cbdb import gcd_models
from cbdb import tgd_models


# Connect to the GCD database
DB = gcd_db.Database()
DB.connect()

# Read in txt file with barcode per line
barcodes = list()
with open("cbdb/example_barcodes.txt") as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        barcodes.append(l)

for barcode in barcodes:
    # Lookup a comic using GCD issue ID
    issues = DB.search_barcode(barcode)

    if issues:
        comic_dict = dict()
        # For simplicity, select first hit
        # There will be duplicates, and this needs better handling
        issue_dict = issues[0]
        # Find the associated comic series
        series_id = str(issue_dict["series_id"])
        series_dict = DB.fetch_series_using_id(series_id)
        # Find the associated comic publisher
        publisher_id = str(series_dict["publisher_id"])
        publisher_dict = DB.fetch_publisher_using_id(publisher_id)
        # Create GCD object from GCD data
        gcd_issue = gcd_models.Issue(**issue_dict)
        gcd_series = gcd_models.Series(**series_dict)
        gcd_publisher = gcd_models.Publisher(**publisher_dict)
        # Make new dict for import
        comic_dict = publisher_dict.copy()
        comic_dict.update(series_dict)
        comic_dict.update(issue_dict)
        comic_dict["series_name"] = series_dict["name"]
        comic_dict["publisher_name"] = publisher_dict["name"]
        # comic_dict
        tgd_comic = tgd_models.Comic(**comic_dict)
        tgd_comic.print_for_spreadsheet()
    else:
        print(f"{barcode}\tNONE")
