from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Publisher(BaseModel):
    id: int
    name: int
    year_began: int
    year_ended: int
    series_count: int


class Series(BaseModel):
    id: int
    name: int
    year_began: int
    year_ended: int
    first_issue_id: int
    last_issue_id: int
    publisher_id: int
    issue_count: int


class Issue(BaseModel):
    id: int
    number: Optional[int] = None
    volume: str
    title: str
    series_id: int
    published_id: int
    brand_id: int
    publication_date: Optional[datetime] = None
    price: str
    isbn: str
    variant_of_id: int = None
    variant_name: str = None
    barcode: str


class Comic(BaseModel):
    id: int
    number: Optional[int] = None
    volume: str
    title: str
    publication_date: Optional[datetime] = None
    price: str
    isbn: str
    variant_of_id: int = None
    variant_name: str = None
    barcode: str
    publisher_name: str
    series_name: str
    series_year_began: int
    series_year_ended: Optional[int] = None
    series_first_issue_id: int
    series_last_issue_id: int

    def print_gcd_style_title(self):
        """Print line to match GCD style comic naming conventions"""
        if self.variant_name:
            print(f"{self.series_name} ({self.publisher_name}, {self.series_year_began} series) #{self.number} [{self.variant_name}]")
        else:
            print(f"{self.series_name} ({self.publisher_name}, {self.series_year_began} series) #{self.number}")

    def print_for_spreadsheet(self):
        """Print line to be pasted into my personal spreadsheet"""
        print(
            f"{self.barcode}\t{self.id}\t{self.series_name}\t{self.series_year_began}\t{self.number}"
        )

def populate(issue_dict, series_dict, publisher_dict):
    temp_dict = {
        "id": issue_dict["id"],
        "number": issue_dict["number"],
        "volume": issue_dict["volume"],
        "title": issue_dict["title"],
        "publication_date": issue_dict["publication_date"],
        "price": issue_dict["price"],
        "isbn": issue_dict["isbn"],
        "variant_of_id": issue_dict["variant_of_id"],
        "variant_name": issue_dict["variant_name"],
        "barcode": issue_dict["barcode"],
        "publisher_name": publisher_dict["name"],
        "series_name": series_dict["name"],
        "series_year_began": series_dict["year_began"],
        "series_year_ended": series_dict["year_ended"],
        "series_first_issue_id": series_dict["first_issue_id"],
        "series_last_issue_id": series_dict["last_issue_id"],
    }
    return temp_dict
