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

    def populate(self, issue_dict, series_dict, publisher_dict):
        """Populate object using issue/series data"""
        self.populate_from_issue_data(issue_dict)
        self.populate_from_series_data(series_dict)
        self.populate_from_publisher_data(publisher_dict)

    def populate_from_issue_data(self, issue_dict):
        """Pop object using dict from GCD issue query"""
        self.issue_id = issue_dict["id"]
        self.series_id = issue_dict["series_id"]
        self.issue_number = issue_dict["number"]
        self.volume_number = issue_dict["volume"]
        self.publication_date = issue_dict["publication_date"]
        self.barcode = issue_dict["barcode"]
        self.title = issue_dict["title"]
        self.variant_name = issue_dict["variant_name"]
        self.on_sale_date = issue_dict["on_sale_date"]
        self.variant_of_id = issue_dict["variant_of_id"]

    def populate_from_series_data(self, series_dict):
        """Pop object using dict from GCD series query"""
        self.series_name = series_dict["name"]
        self.year_began = series_dict["year_began"]
        self.publisher_id = series_dict["publisher_id"]

    def populate_from_publisher_data(self, publisher_dict):
        """Pop object using dict from GCD publisher query"""
        self.publisher_name = publisher_dict["name"]

    def print_for_spreadsheet(self):
        """Print line to be pasted into my spreadsheet"""
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
