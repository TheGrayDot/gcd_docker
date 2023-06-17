from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Comic(BaseModel):
    # Issue
    id: int = None
    number: str = None
    volume: str = ""
    series_id: int = None
    publication_date: datetime = None
    price: str = None
    page_count: Optional[float] = None
    deleted: int = 0
    isbn: str = ""
    valid_isbn: str = ""
    no_isbn: int = 0
    variant_of_id: Optional[int] = None
    variant_name: str = ""
    barcode: str = ""
    no_barcode: int = 0
    title: str = ""
    no_title: int = 0
    on_sale_date: str = None
    on_sale_date_uncertain: int = 0
    # Series
    series_name: str = None  # non-default name
    year_began: int = None
    year_began_uncertain: int = 0
    year_ended: Optional[int] = None
    year_ended_uncertain: int = 0
    first_issue_id: Optional[int] = None
    last_issue_id: Optional[int] = None
    country_id: int = None
    language_id: int = None
    has_gallery: int = 0
    issue_count: int = None
    has_isbn: int = 1
    has_barcode: int = 1
    has_issue_title: int = 0
    color: str = None
    dimensions: str = None
    paper_stock: str = None
    binding: str = None
    publishing_format: str = None
    # Publisher
    publisher_name: str = None  # non-default name

    def print_gcd_style_title(self):
        """Print line to match GCD style comic naming conventions"""
        if self.variant_name:
            print(
                f"{self.series_name} ({self.publisher_name}, {self.year_began} series) #{self.number} [{self.variant_name}]"
            )
        else:
            print(
                f"{self.series_name} ({self.publisher_name}, {self.year_began} series) #{self.number}"
            )

    def print_for_spreadsheet(self):
        """Print line to be pasted into my personal spreadsheet"""
        print(
            f"{self.barcode}\t{self.id}\t{self.series_name}\t{self.year_began}\t{self.number}"
        )
