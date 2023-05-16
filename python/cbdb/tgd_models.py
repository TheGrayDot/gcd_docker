from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Comic(BaseModel):
    id: int
    number: Optional[int] = None
    number: str
    volume: str
    title: str
    publication_date: Optional[datetime] = None
    publication_date: str
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
            print(
                f"{self.series_name} ({self.publisher_name}, {self.series_year_began} series) #{self.number} [{self.variant_name}]"
            )
        else:
            print(
                f"{self.series_name} ({self.publisher_name}, {self.series_year_began} series) #{self.number}"
            )

    def print_for_spreadsheet(self):
        """Print line to be pasted into my personal spreadsheet"""
        print(
            f"{self.barcode}\t{self.id}\t{self.series_name}\t{self.series_year_began}\t{self.number}"
        )
