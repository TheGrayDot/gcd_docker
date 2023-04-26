import db
import comic


# Connect to the GCD database
gcd_db = db.Database()
gcd_db.connect()

# Lookup all issues using GCD series ID
series_id = "4611"  # Spawn
issues = gcd_db.fetch_issue_using_series_id(series_id)
print("ISSUE DICTIONARY")
print(len(issues))
