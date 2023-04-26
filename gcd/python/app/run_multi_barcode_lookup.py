import db
import comic


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
        # For simplicity, select first hit
        # There will be duplicates, and this needs better handling
        issue = issues[0]
        series_id = str(issue["series_id"])
        series = gcd_db.fetch_series_using_id(series_id)
        # Find the associated comic publisher
        publisher_id = str(series["publisher_id"])
        publisher = gcd_db.fetch_publisher_using_id(publisher_id)
        # Use issue/series/publisher info to make a comic object
        comic_obj = comic.Comic()
        comic_obj.populate(issue, series, publisher)
        comic_obj.print_for_spreadsheet()
        # comic_obj.print_gcd_style_title()
    else:
        print(f"{barcode}\tNONE")
