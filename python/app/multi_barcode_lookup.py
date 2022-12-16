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
    issue_dicts = gcd_db.search_barcode(barcode)
    # TODO: Could do something here to just process one
    for issue_dict in issue_dicts:
        # Find the associated comic series
        series_id = str(issue_dict["series_id"])
        series_dict = gcd_db.fetch_series_dict_using_id(series_id)
        # Find the associated comic publisher
        publisher_id = str(series_dict["publisher_id"])
        publisher_dict = gcd_db.fetch_publisher_dict_using_id(publisher_id)
        # Use issue/series/publisher info to make a comic object
        comic_obj = comic.Comic()
        comic_obj.populate(issue_dict, series_dict, publisher_dict)
        comic_obj.print_for_spreadsheet()
        comic_obj.print_gcd_style_title()
