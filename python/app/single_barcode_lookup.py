import os
import sys

import mysql.connector


# Check an argument was supplied
if len(sys.argv) < 2:
    print("[*] Error: You must supply a comic barcode as a first argument. Exiting.")
    exit(1)

# Connect to MySQL database
print("[*] Connecting to MySQL database")
gcd_db = mysql.connector.connect(
    host="gcd_mysql",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

barcode = sys.argv[1]
print(f"[*] Searching barcode: {barcode}")

# Query gcd_issue table for specific barcode
issue_query = f"SELECT series_id, number FROM gcd_issue WHERE barcode = '{barcode}' LIMIT 10"
with gcd_db.cursor() as cursor:
    cursor.execute(issue_query)
    issues = cursor.fetchall()
    # Check if a result was found (aka matching barcode for an issue)
    if issues:
        print("[*] Found the following match/es...")
        for issue in issues:
            issue_series_id = issue[0]
            issue_number = issue[1]
            # Based on series_id we got, lookup the comic series
            series_query = f"SELECT name, year_began FROM gcd_series WHERE id = '{issue_series_id}'"
            with gcd_db.cursor() as cursor:
                cursor.execute(series_query)
                series = cursor.fetchone()
                series_name = series[0]
                series_year_began = series[1]
                print(f'[*] {series_name} ({series_year_began}) issue {issue_number}')
    else:
        print("[*] Sorry, barcode not found. Exiting.")
