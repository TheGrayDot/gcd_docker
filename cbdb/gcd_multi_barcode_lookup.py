from cbdb import gcd_db
from cbdb import comic


# Connect to the GCD database
db = gcd_db.Database()
db.connect()

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
    issues = db.search_barcode(barcode)
    
    if issues:
        comic_dict = dict()
        # For simplicity, select first hit
        # There will be duplicates, and this needs better handling
        issue_dict = issues[0]
        # Find the associated comic series
        series_id = str(issue_dict["series_id"])
        series_dict = db.fetch_series_using_id(series_id)
        # Find the associated comic publisher
        publisher_id = str(series_dict["publisher_id"])
        publisher_dict = db.fetch_publisher_using_id(publisher_id)
        # Create Comic object from GCD data
        comic_dict = comic.populate(issue_dict, series_dict, publisher_dict)
        comic_obj = comic.Comic.parse_obj(comic_dict)
        comic_obj.print_for_spreadsheet()
    else:
        print(f"{barcode}\tNONE")
