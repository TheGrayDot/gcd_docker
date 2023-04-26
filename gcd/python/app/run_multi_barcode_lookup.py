import db
from model import comic


# Connect to the GCD database
gcd_db = db.Database()
gcd_db.connect()

# Read in txt file with barcode per line
barcodes = list()
with open("example_barcodes.txt") as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        barcodes.append(l)

for barcode in barcodes:
    # Lookup a comic using GCD issue ID
    issues = gcd_db.search_barcode(barcode)
    
    if issues:
        comic_dict = dict()
        # For simplicity, select first hit
        # There will be duplicates, and this needs better handling
        issue_dict = issues[0]
        # Find the associated comic series
        series_id = str(issue_dict["series_id"])
        series_dict = gcd_db.fetch_series_using_id(series_id)
        # Find the associated comic publisher
        publisher_id = str(series_dict["publisher_id"])
        publisher_dict = gcd_db.fetch_publisher_using_id(publisher_id)
        # Create Comic object from GCD data
        comic_dict = comic.create_comic_dict_from_gcd_data(issue_dict, series_dict, publisher_dict)
        comic_obj = comic.Comic.parse_obj(comic_dict)
        comic_obj.print_for_spreadsheet()
    else:
        print(f"{barcode}\tNONE")
