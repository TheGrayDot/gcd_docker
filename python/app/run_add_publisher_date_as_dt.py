import datetime

import dateparser
import mysql.connector

import db


TODAY_DT = datetime.datetime.now().strftime("%Y-%m-%d")

DP_SETTINGS = {
    "PREFER_DAY_OF_MONTH": "first",
    "REQUIRE_PARTS": ["year"]
}

# Connect to the GCD database
gcd_db = db.Database()
gcd_db.connect()

# Remove table column, for testing
# ALTER TABLE gcd_issue DROP COLUMN publication_date_dt;

# Create new column in gcd_issue
print("[*] Creating new column")
query = "ALTER TABLE gcd_issue ADD publication_date_dt DATETIME DEFAULT NULL"
try:
    with gcd_db.gcd_db.cursor(dictionary=True) as cursor:
        cursor.execute(query)
except mysql.connector.Error:
    # Skip error when column already exists
    # _mysql_connector.MySQLInterfaceError: Duplicate column name 'publication_date_dt'
    pass

# Determine issue count
print("[*] Determining row count...")
row_count = 0
query = "SELECT * FROM gcd_issue"
with gcd_db.gcd_db.cursor() as cursor:
    cursor.execute(query)
    cursor.fetchall()
    row_count = cursor.rowcount
print(f"[*] row_count: {row_count}")
# row_count = 2275369

# Paginate through all issues
print("[*] Starting")
offset = 0
limit = 1000
 
while offset < row_count:
    print(f"[*] offset: {offset}")
    # print(f"[*] row_count: {row_count}")

    issues = gcd_db.paginate_all_issues(limit, offset)
    # print(f"[*] len(issues): {len(issues)}")

    offset += limit
    issues_updated = list()

    # For each issue in paginated list, update publication date timestamp to object
    for issue in issues:
        issue_id = int(issue["id"])
        # print(f"[*] issue_id: {issue_id}")

        publication_date = issue["publication_date"]
        # print(f"[*] publication_date: {publication_date}")

        publication_dt = dateparser.parse(publication_date, settings=DP_SETTINGS)
        # print(f"[*] publication_dt: {publication_dt}")

        if publication_dt:
            publication_dt_str = publication_dt.strftime('%Y-%m-%d %H:%M:%S')

        if publication_dt_str:
            # dateparser returns today's date if not found
            # So, set it to None instead
            if publication_dt_str.startswith(TODAY_DT):
                publication_dt_str = None

        # Create tuple to update
        # (publication datetime string, issue ID number)
        temp_tuple = (publication_dt_str, issue_id)

        # Add update tuple to list
        issues_updated.append(temp_tuple)
    
    # Bulk update all changed issues with new datetime column
    query = "UPDATE gcd_issue SET publication_date_dt = %s WHERE id = %s"
    with gcd_db.gcd_db.cursor(dictionary=True) as cursor:
        cursor.executemany(query, issues_updated)
        gcd_db.gcd_db.commit()

print("[*] Done")
