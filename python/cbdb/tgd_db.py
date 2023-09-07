import os

import mysql.connector


class Database:
    def __init__(self):
        self.tgd_db = None

    def connect(self):
        self.tgd_db = mysql.connector.connect(
            host="tgd-mysql",
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )

    def search_barcode(self, barcode: str, limit: str = 100):
        query = """SELECT * FROM comics
                   WHERE barcode = %s LIMIT %s"""
        with self.tgd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (barcode, limit))
            issues = cursor.fetchall()
            return issues

    def fecth_all_issues(self):
        query = "SELECT * FROM comics"
        with self.tgd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            issues = cursor.fetchall()
            return issues

    def paginate_all_issues(self, limit: int, offset: int):
        query = """SELECT * FROM comics
                   ORDER BY id LIMIT %s OFFSET %s"""
        with self.tgd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (limit, offset))
            issues = cursor.fetchall()
            return issues

    def paginate_all_issues_with_series(self, limit: int, offset: int):
        query = """SELECT * FROM comics
                   ORDER BY id LIMIT %s OFFSET %s"""
        with self.tgd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (limit, offset))
            issues = cursor.fetchall()
            return issues

    def fetch_issue_using_id(self, issue_id: int):
        query = """SELECT * FROM comics
                   WHERE id = %s LIMIT 1"""
        with self.tgd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (issue_id,))
            issue = cursor.fetchall()
            return issue[0]

    def fetch_issue_using_series_id(self, series_id: int):
        query = """SELECT * FROM comics
                   WHERE series_id = %s AND variant_of_id IS NULL"""
        with self.tgd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (series_id,))
            issues = cursor.fetchall()
            return issues

    def fetch_series_using_id(self, series_id: str):
        query = """SELECT * FROM comics
                   WHERE id = %s LIMIT 1"""
        with self.tgd_db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (series_id,))
            series = cursor.fetchall()
            return series[0]
