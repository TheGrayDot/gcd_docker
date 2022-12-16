# gcd_sql_structure

Some notes on the SQL database structure in the GCD project.

## All Tables

```
mysql> show tables;
+-----------------------------------+
| Tables_in_gcd                     |
+-----------------------------------+
| django_content_type               |
| gcd_award                         |
| gcd_biblio_entry                  |
| gcd_brand                         |
| gcd_brand_emblem_group            |
| gcd_brand_group                   |
| gcd_brand_use                     |
| gcd_creator                       |
| gcd_creator_art_influence         |
| gcd_creator_degree                |
| gcd_creator_membership            |
| gcd_creator_name_detail           |
| gcd_creator_non_comic_work        |
| gcd_creator_relation              |
| gcd_creator_relation_creator_name |
| gcd_creator_school                |
| gcd_creator_signature             |
| gcd_credit_type                   |
| gcd_degree                        |
| gcd_feature                       |
| gcd_feature_logo                  |
| gcd_feature_logo_2_feature        |
| gcd_feature_relation              |
| gcd_feature_relation_type         |
| gcd_feature_type                  |
| gcd_indicia_printer               |
| gcd_indicia_publisher             |
| gcd_issue                         |
| gcd_issue_credit                  |
| gcd_issue_indicia_printer         |
| gcd_membership_type               |
| gcd_name_type                     |
| gcd_non_comic_work_role           |
| gcd_non_comic_work_type           |
| gcd_non_comic_work_year           |
| gcd_printer                       |
| gcd_publisher                     |
| gcd_received_award                |
| gcd_relation_type                 |
| gcd_reprint                       |
| gcd_school                        |
| gcd_series                        |
| gcd_series_bond                   |
| gcd_series_bond_type              |
| gcd_series_publication_type       |
| gcd_story                         |
| gcd_story_credit                  |
| gcd_story_feature_logo            |
| gcd_story_feature_object          |
| gcd_story_type                    |
| stddata_country                   |
| stddata_date                      |
| stddata_language                  |
| stddata_script                    |
| taggit_tag                        |
| taggit_taggeditem                 |
+-----------------------------------+
```

## Issue Table

Represents a single comic book (1 issue). For example, The Amazing Spider-man issue 300.

```
mysql> DESCRIBE gcd_issue;
+----------------------------+---------------+------+-----+---------------------+----------------+
| Field                      | Type          | Null | Key | Default             | Extra          |
+----------------------------+---------------+------+-----+---------------------+----------------+
| id                         | int           | NO   | PRI | NULL                | auto_increment |
| number                     | varchar(50)   | NO   | MUL | NULL                |                |
| volume                     | varchar(50)   | NO   | MUL |                     |                |
| no_volume                  | tinyint(1)    | NO   | MUL | 0                   |                |
| display_volume_with_number | tinyint(1)    | NO   | MUL | 0                   |                |
| series_id                  | int           | NO   | MUL | NULL                |                |
| indicia_publisher_id       | int           | YES  | MUL | NULL                |                |
| indicia_pub_not_printed    | tinyint(1)    | NO   |     | NULL                |                |
| brand_id                   | int           | YES  | MUL | NULL                |                |
| no_brand                   | tinyint(1)    | NO   | MUL | NULL                |                |
| publication_date           | varchar(255)  | NO   |     | NULL                |                |
| key_date                   | varchar(10)   | NO   | MUL | NULL                |                |
| sort_code                  | int           | NO   | MUL | NULL                |                |
| price                      | varchar(255)  | NO   |     | NULL                |                |
| page_count                 | decimal(10,3) | YES  |     | NULL                |                |
| page_count_uncertain       | tinyint(1)    | NO   |     | 0                   |                |
| indicia_frequency          | varchar(255)  | NO   |     |                     |                |
| no_indicia_frequency       | tinyint(1)    | NO   | MUL | 0                   |                |
| editing                    | longtext      | NO   |     | NULL                |                |
| no_editing                 | tinyint(1)    | NO   | MUL | 0                   |                |
| notes                      | longtext      | NO   |     | NULL                |                |
| created                    | datetime      | NO   |     | 1901-01-01 00:00:00 |                |
| modified                   | datetime      | NO   | MUL | 1901-01-01 00:00:00 |                |
| deleted                    | tinyint(1)    | NO   | MUL | 0                   |                |
| is_indexed                 | tinyint(1)    | NO   | MUL | 0                   |                |
| isbn                       | varchar(32)   | NO   | MUL |                     |                |
| valid_isbn                 | varchar(13)   | NO   | MUL |                     |                |
| no_isbn                    | tinyint(1)    | NO   | MUL | 0                   |                |
| variant_of_id              | int           | YES  | MUL | NULL                |                |
| variant_name               | varchar(255)  | NO   |     |                     |                |
| barcode                    | varchar(38)   | NO   | MUL |                     |                |
| no_barcode                 | tinyint(1)    | NO   |     | 0                   |                |
| title                      | varchar(255)  | NO   | MUL |                     |                |
| no_title                   | tinyint(1)    | NO   | MUL | 0                   |                |
| on_sale_date               | varchar(10)   | NO   | MUL | NULL                |                |
| on_sale_date_uncertain     | tinyint(1)    | NO   |     | 0                   |                |
| rating                     | varchar(255)  | NO   | MUL | NULL                |                |
| no_rating                  | tinyint(1)    | NO   | MUL | NULL                |                |
| volume_not_printed         | tinyint(1)    | NO   |     | NULL                |                |
| no_indicia_printer         | tinyint(1)    | NO   |     | NULL                |                |
+----------------------------+---------------+------+-----+---------------------+----------------+\
```

## Series Tables

Represents a comic book series (multiple issues). For example, The Amazing Spider-man.

```
mysql> DESCRIBE gcd_series;
+---------------------------+--------------+------+-----+---------------------+----------------+
| Field                     | Type         | Null | Key | Default             | Extra          |
+---------------------------+--------------+------+-----+---------------------+----------------+
| id                        | int          | NO   | PRI | NULL                | auto_increment |
| name                      | varchar(255) | NO   | MUL | NULL                |                |
| sort_name                 | varchar(255) | NO   | MUL | NULL                |                |
| format                    | varchar(255) | NO   |     |                     |                |
| year_began                | int          | NO   | MUL | NULL                |                |
| year_began_uncertain      | tinyint(1)   | NO   |     | 0                   |                |
| year_ended                | int          | YES  |     | NULL                |                |
| year_ended_uncertain      | tinyint(1)   | NO   |     | 0                   |                |
| publication_dates         | varchar(255) | NO   |     |                     |                |
| first_issue_id            | int          | YES  | MUL | NULL                |                |
| last_issue_id             | int          | YES  | MUL | NULL                |                |
| is_current                | tinyint(1)   | NO   | MUL | 0                   |                |
| publisher_id              | int          | NO   | MUL | NULL                |                |
| country_id                | int          | NO   | MUL | NULL                |                |
| language_id               | int          | NO   | MUL | NULL                |                |
| tracking_notes            | longtext     | NO   |     | NULL                |                |
| notes                     | longtext     | NO   |     | NULL                |                |
| has_gallery               | tinyint(1)   | NO   | MUL | 0                   |                |
| issue_count               | int          | NO   |     | NULL                |                |
| created                   | datetime     | NO   |     | 1901-01-01 00:00:00 |                |
| modified                  | datetime     | NO   | MUL | 1901-01-01 00:00:00 |                |
| deleted                   | tinyint(1)   | NO   | MUL | 0                   |                |
| has_indicia_frequency     | tinyint(1)   | NO   |     | 1                   |                |
| has_isbn                  | tinyint(1)   | NO   |     | 1                   |                |
| has_barcode               | tinyint(1)   | NO   |     | 1                   |                |
| has_issue_title           | tinyint(1)   | NO   |     | 0                   |                |
| has_volume                | tinyint(1)   | NO   |     | 1                   |                |
| is_comics_publication     | tinyint(1)   | NO   |     | 1                   |                |
| color                     | varchar(255) | NO   |     | NULL                |                |
| dimensions                | varchar(255) | NO   |     | NULL                |                |
| paper_stock               | varchar(255) | NO   |     | NULL                |                |
| binding                   | varchar(255) | NO   |     | NULL                |                |
| publishing_format         | varchar(255) | NO   |     | NULL                |                |
| has_rating                | tinyint(1)   | NO   |     | NULL                |                |
| publication_type_id       | int          | YES  | MUL | NULL                |                |
| is_singleton              | tinyint(1)   | NO   |     | NULL                |                |
| has_about_comics          | tinyint(1)   | NO   |     | NULL                |                |
| has_indicia_printer       | tinyint(1)   | NO   |     | NULL                |                |
| has_publisher_code_number | tinyint(1)   | NO   |     | NULL                |                |
+---------------------------+--------------+------+-----+---------------------+----------------+
```

## Example Queries

Lookup a comic issue with a specific barcode (including supplementary 2-5 digit code):

```
SELECT * FROM gcd_issue WHERE barcode = '75960608629004011';
```

Lookup a comic series using a specific `series_id` (found in the previous example):

```
SELECT * FROM gcd_series WHERE id = '110055';
```
