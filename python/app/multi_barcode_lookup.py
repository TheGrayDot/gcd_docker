import os
import sys

import mysql.connector


barcodes = list()
with open("barcodes.txt") as f:
    for l in f:
        l = l.strip()
        barcodes.append(l)

# Connect to MySQL database
print("[*] Connecting to MySQL database")
gcd_db = mysql.connector.connect(
    host="gcd_mysql",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

for barcode in barcodes:
    # Query gcd_issue table for specific barcode
    issue_query = f"SELECT id, series_id, number FROM gcd_issue WHERE barcode = '{barcode}' LIMIT 10"
    with gcd_db.cursor() as cursor:
        cursor.execute(issue_query)
        issues = cursor.fetchall()
        # Check if a result was found (aka matching barcode for an issue)
        if issues:
            for issue in issues:
                issue_id = issue[0]
                issue_series_id = issue[1]
                issue_number = issue[2]
                # Based on series_id we got, lookup the comic series
                series_query = f"SELECT name, year_began FROM gcd_series WHERE id = '{issue_series_id}'"
                with gcd_db.cursor() as cursor:
                    cursor.execute(series_query)
                    series = cursor.fetchone()
                    series_name = series[0]
                    series_year_began = series[1]
                    print(f'{issue_id}\t{series_name}\t{series_year_began}\t{issue_number}')
        else:
            print()
