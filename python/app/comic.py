import datetime

import dateparser

import db


class Comic:
    def __init__(self):
        # Properties from issue table
        self.issue_id = None
        self.series_id = None
        self.issue_number = None
        self.volume_number = None
        self.publication_date = None
        self.barcode = None
        self.title = None
        self.variant_name = None
        self.on_sale_date = None
        self.variant_of_id = None
        # Properties from series table
        self.series_name = None
        self.year_began = None
        self.publisher_id = None
        # Properties from publisher table
        self.publisher_name = None

    def to_json(self):
        data = {
            "issue_id": self.issue_id,
            "series_id": self.series_id,
            "issue_number": self.issue_number,
            "volume_number": self.volume_number,
            "publication_date": self.publication_date,
            "barcode": self.barcode,
            "title": self.title,
            "variant_name": self.variant_name,
            "on_sale_date": self.on_sale_date,
            "variant_of_id": self.variant_of_id,
            "series_name": self.series_name,
            "year_began": self.year_began,
            "publisher_id": self.publisher_id,
            "publisher_name": self.publisher_name
        }
        return data

    def populate(self, issue, series, publisher):
        """Populate object using issue/series data"""
        self.populate_from_issue_data(issue)
        self.populate_from_series_data(series)
        self.populate_from_publisher_data(publisher)

    def populate_from_issue_data(self, issue):
        """Pop object using dict from GCD issue query"""
        self.issue_id = issue["id"]
        self.series_id = issue["series_id"]
        self.issue_number = issue["number"]
        self.volume_number = issue["volume"]
        self.publication_date = issue["publication_date"]
        self.barcode = issue["barcode"]
        self.title = issue["title"]
        self.variant_name = issue["variant_name"]
        self.on_sale_date = issue["on_sale_date"]
        self.variant_of_id = issue["variant_of_id"]

    def populate_from_series_data(self, series):
        """Pop object using dict from GCD series query"""
        self.series_name = series["name"]
        self.year_began = series["year_began"]
        self.publisher_id = series["publisher_id"]

    def populate_from_publisher_data(self, publisher):
        """Pop object using dict from GCD publisher query"""
        self.publisher_name = publisher["name"]

    def print_for_spreadsheet(self):
        """Print line to be pasted into my personal spreadsheet"""
        print(
            f"{self.barcode}\t{self.issue_id}\t{self.series_name}\t{self.year_began}\t{self.issue_number}"
        )

    def print_gcd_style_title(self):
        """Print line to match GCD style comic naming conventions"""
        if self.variant_name:
            print(f"{self.series_name} ({self.publisher_name}, {self.year_began} series) #{self.issue_number} [{self.variant_name}]")
        else:
            print(f"{self.series_name} ({self.publisher_name}, {self.year_began} series) #{self.issue_number}")

    def print_mycomicshop_style_title(self):
        """"""
        pass
