from cbdb import gcd_db


# Connect to the GCD database
db = gcd_db.Database()
db.connect()

# Lookup all issues using GCD series ID
series_id = "4611"  # Spawn
issues = db.fetch_issue_using_series_id(series_id)
print("ISSUE DICTIONARY")
print(len(issues))
