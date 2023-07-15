import os

import mysql.connector


class Database:
    def __init__(self):
        self.gcd_db = None

    def connect(self):
        self.gcd_db = mysql.connector.connect(
            host="gcd_mysql",
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )

    def search_barcode(self, barcode: str, limit: str = 100):
        query = """SELECT * FROM gcd_issue
                   WHERE barcode = %s LIMIT %s"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (barcode, limit))
            issues = cursor.fetchall()
            return issues

    def fecth_all_issues(self):
        query = "SELECT * FROM gcd_issue"
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            issues = cursor.fetchall()
            return issues

    def paginate_all_issues(self, limit: int, offset: int):
        query = """SELECT * FROM gcd_issue
                   ORDER BY id LIMIT %s OFFSET %s"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (limit, offset))
            issues = cursor.fetchall()
            return issues

    def paginate_all_issues_with_series(self, limit: int, offset: int):
        query = """SELECT * FROM gcd_issue
                   ORDER BY id LIMIT %s OFFSET %s"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (limit, offset))
            issues = cursor.fetchall()
            return issues

    def fetch_issue_using_id(self, issue_id: int):
        query = """SELECT * FROM gcd_issue
                   WHERE id = %s LIMIT 1"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (issue_id,))
            issue = cursor.fetchall()
            return issue[0]

    def fetch_issue_using_series_id(self, series_id: int):
        query = """SELECT * FROM gcd_issue
                   WHERE series_id = %s AND variant_of_id IS NULL"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (series_id,))
            issues = cursor.fetchall()
            return issues

    def fetch_series_using_id(self, series_id: str):
        query = """SELECT * FROM gcd_series
                   WHERE id = %s LIMIT 1"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (series_id,))
            series = cursor.fetchall()
            return series[0]

    def fetch_publisher_using_id(self, publisher_id: str):
        query = """SELECT * FROM gcd_publisher
                   WHERE id = %s LIMIT 1"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (publisher_id,))
            publisher = cursor.fetchall()
            return publisher[0]

    def paginate_all_publishers(self, limit: int, offset: int):
        query = """SELECT * FROM gcd_publisher
                   ORDER BY id LIMIT %s OFFSET %s"""
        with self.gcd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (limit, offset))
            publishers = cursor.fetchall()
            return publishers
