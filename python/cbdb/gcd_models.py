from datetime import datetime
from typing import Optional
from pydantic import BaseModel


DEFAULT_DT = datetime.strptime("1901-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")


class Publisher(BaseModel):
    id: int
    name: str
    country_id: int
    year_began: Optional[int] = None
    year_ended: Optional[int] = None
    notes: str
    url: str
    brand_count: int = 0
    indicia_publisher_count: int = 0
    series_count: int = 0
    created: datetime = DEFAULT_DT
    modified: datetime = DEFAULT_DT
    issue_count: int = 0
    deleted: int = 0
    year_began_uncertain: int = 0
    year_ended_uncertain: int = 0
    year_overall_began: Optional[int] = None
    year_overall_began_uncertain: int
    year_overall_ended: Optional[int] = None
    year_overall_ended_uncertain: int


class Series(BaseModel):
    id: int
    name: str
    sort_name: str
    format: str = ""
    year_began: int
    year_began_uncertain: int = 0
    year_ended: Optional[int] = None
    year_ended_uncertain: int = 0
    publication_dates: str = ""
    first_issue_id: Optional[int] = None
    last_issue_id: Optional[int] = None
    is_current: int = 0
    publisher_id: int
    country_id: int
    language_id: int
    tracking_notes: str 
    notes: str
    has_gallery: int = 0
    issue_count: int
    created: datetime = DEFAULT_DT
    modified: datetime = DEFAULT_DT
    deleted: int = 0
    has_indicia_frequency: int = 1
    has_isbn: int = 1
    has_barcode: int = 1
    has_issue_title: int = 0
    has_volume: int = 1
    is_comics_publication: int = 1
    color: str
    dimensions: str
    paper_stock: str
    binding: str
    publishing_format: str
    has_rating: int
    publication_type_id: Optional[int]
    is_singleton: int
    has_about_comics: int
    has_indicia_printer: int
    has_publisher_code_number: int


class Issue(BaseModel):
    id: int
    number: str
    volume: str = ""
    no_volume: int = 0
    display_volume_with_number: int = 0
    series_id: int
    indicia_publisher_id: Optional[int] = None
    indicia_pub_not_printed: int
    brand_id: Optional[int] = None
    no_brand: int
    publication_date: str
    key_date: str
    sort_code: int
    price: str
    page_count: Optional[float] = None
    page_count_uncertain: int = 0
    indicia_frequency: str = ""
    no_indicia_frequency: int = 0
    editing: str
    no_editing: int = 0
    notes: str
    created: datetime = DEFAULT_DT
    modified: datetime = DEFAULT_DT
    deleted: int = 0
    is_indexed: int = 0
    isbn: str = ""
    valid_isbn: str = ""
    no_isbn: int = 0
    variant_of_id: Optional[int] = None
    variant_name: str = ""
    barcode: str = ""
    no_barcode: int = 0
    title: str = ""
    no_title: int = 0
    on_sale_date: str
    on_sale_date_uncertain: int = 0
    rating: str
    no_rating: int
    volume_not_printed: int
    no_indicia_printer: int
