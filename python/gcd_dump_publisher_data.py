import json
import datetime

from cbdb import gcd_db


# Connect to the GCD database
db = gcd_db.Database()
db.connect()

# Determine issue count
print("[*] Determining row count...")
row_count = 0
query = "SELECT * FROM gcd_publisher"
with db.gcd_db.cursor() as cursor:
    cursor.execute(query)
    cursor.fetchall()
    row_count = cursor.rowcount
print(f"[*] row_count: {row_count}")

# Paginate through all publishers
print("[*] Starting")
offset = 0
limit = 100

# Dict to save publisher ID > publisher name
publishers_dict = dict()
 
while offset < row_count:
    print(f"[*] offset: {offset}")
    publishers = db.paginate_all_publishers(limit, offset)
    print(f"[*] len(publishers): {len(publishers)}")

    offset += limit

    # For each publisher in paginated list, fetch needed data
    for publisher_dict in publishers:
        publisher_id = int(publisher_dict["id"])
        print(f"[*] {publisher_id}")
        publisher_name = publisher_dict["name"]
        publishers_dict[publisher_id] = publisher_name

# Save dict to JSON file
with open("cbdb/publishers.json", "w") as f:
    json.dump(publishers_dict, f, indent=4)

print("[*] Done")
