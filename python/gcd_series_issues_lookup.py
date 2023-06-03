from cbdb import gcd_db


# Connect to the GCD database
DB = gcd_db.Database()
DB.connect()

# Lookup all issues using GCD series ID
series_id = "4611"  # Spawn
issues = DB.fetch_issue_using_series_id(series_id)
print(len(issues))
