import datetime

from cbdb import gcd_db
from cbdb import gcd_models


# Connect to the GCD database
DB = gcd_db.Database()
DB.connect()

# Determine issue count
print("[*] Determining row count...")
row_count = 0
query = "SELECT * FROM gcd_issue"
with DB.gcd_db.cursor() as cursor:
    cursor.execute(query)
    cursor.fetchall()
    row_count = cursor.rowcount
print(f"[*] row_count: {row_count}")

# Paginate through all issues
print("[*] Starting")
offset = 0
limit = 1000

while offset < row_count:
    print(f"[*] offset: {offset}")
    issues = DB.paginate_all_issues(limit, offset)
    print(f"[*] len(issues): {len(issues)}")

    offset += limit
    issues_updated = list()

    # For each issue in paginated list, update publication date timestamp to object
    for issue_dict in issues:
        issue_id = int(issue_dict["id"])
        print(f"[*] {issue_id}")
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

print("[*] Done")
