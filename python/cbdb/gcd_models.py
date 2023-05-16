from datetime import datetime
from typing import Optional
from pydantic import BaseModel


DEFAULT_DT = datetime.strptime("1901-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")


class Publisher(BaseModel):
    id: int = None
    name: str = None
    country_id: int = None
    year_began: Optional[int] = None
    year_ended: Optional[int] = None
    notes: str = None
    url: str = None
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
    year_overall_began_uncertain: int = None
    year_overall_ended: Optional[int] = None
    year_overall_ended_uncertain: int = None


class Series(BaseModel):
    id: int = None
    name: str = None
    sort_name: str = None
    format: str = ""
    year_began: int = None
    year_began_uncertain: int = 0
    year_ended: Optional[int] = None
    year_ended_uncertain: int = 0
    publication_dates: str = ""
    first_issue_id: Optional[int] = None
    last_issue_id: Optional[int] = None
    is_current: int = 0
    publisher_id: int = None
    country_id: int = None
    language_id: int = None
    tracking_notes: str = None
    notes: str = None
    has_gallery: int = 0
    issue_count: int = None
    created: datetime = DEFAULT_DT
    modified: datetime = DEFAULT_DT
    deleted: int = 0
    has_indicia_frequency: int = 1
    has_isbn: int = 1
    has_barcode: int = 1
    has_issue_title: int = 0
    has_volume: int = 1
    is_comics_publication: int = 1
    color: str = None
    dimensions: str = None
    paper_stock: str = None
    binding: str = None
    publishing_format: str = None
    has_rating: int = None
    publication_type_id: Optional[int] = None
    is_singleton: int = None
    has_about_comics: int = None
    has_indicia_printer: int = None
    has_publisher_code_number: int = None


class Issue(BaseModel):
    id: int = None
    number: str = None
    volume: str = ""
    no_volume: int = 0
    display_volume_with_number: int = 0
    series_id: int = None
    indicia_publisher_id: Optional[int] = None
    indicia_pub_not_printed: int = None
    brand_id: Optional[int] = None
    no_brand: int = None
    publication_date: str = None
    key_date: str = None
    sort_code: int = None
    price: str = None
    page_count: Optional[float] = None
    page_count_uncertain: int = 0
    indicia_frequency: str = ""
    no_indicia_frequency: int = 0
    editing: str = None
    no_editing: int = 0
    notes: str = None
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
    on_sale_date: str = None
    on_sale_date_uncertain: int = 0
    rating: str = None
    no_rating: int = None
    volume_not_printed: int = None
    no_indicia_printer: int = None
