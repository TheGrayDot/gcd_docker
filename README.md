# gcd_docker

A simple Dockerised environment for working with the [Grand Comic Database™ (GCD)](https://www.comics.org/), and Python scripts for processing data into a format I work with.

## License

This project uses data courtesy of the [Grand Comics Database™](https://www.comics.org/) under a [Creative Commons Attribution license](LICENSE). For more information, please refer to the [GCD wiki page on Data Distribution](https://docs.comics.org/wiki/Data_Distribution) and the [GCD board decision on licensing](https://docs.comics.org/wiki/GCD_Board_Votes_-_2009#Data_License_and_proper_credit_in_derived_works).

NOTE: At present no data from the GCD, or data from the GCD that has been modified, is currently provided in this repository. However, it is planned that derived data from the GCD will be distributed in this repository in the future. Additionally, since the project uses the GCD database (while not currently distributing any data), it is both logical and ethical to adopt the same license.

## gcd

A simple Docker Compose environment for the [Grand Comic Database (GCD)](https://www.comics.org/) with a Python environment and scripts for interacting with the database.

- Uses Docker to provision containers to load and process GCD data
- MySQL container to auto load the GCD data, and keep database persistent in a volume
- Python container to run simple programs to query database, also mounted as a volume

### Project Requirements

- Docker
- Docker Compose plugin
- GCD DB dump

### QuickStart

- Make sure you have the following installed:
    - Docker
    - Docker Compose plugin
- Clone the repo
    - `git clone https://github.com/TheGrayDot/gcd_docker.git && cd ./gcd_docker`
- Copy a GCD MySQL dump to the `data/gcd` folder
    - `cd ~/Downloads && unzip ~/Downloads/current.zip && cp ~/Downloads/2022-01-25.sql ./data/gcd/`
- Start Docker environment
    - `make run`
    - OR
    - `docker compose up --file docker-compose_gcd.yml --build`
- Run a Python script in the Docker container:
    - `docker exec gcd-python python gcd_test_load_all_into_models.py`

### GCD DB Dump

You need to add the GCD DB `.sql` file to load data into the MySQL database. You can download from the following URL (GCD account needed):

- [https://www.comics.org/download/](https://www.comics.org/download/)

Unzip the download, and you will get an `.sql` file in the following format:

```
YYYY-MM-DD.sql
```

For example:

```
2022-01-25.sql
```

To auto-load data in the Docker environment, you will need to put the downloaded and extracted `.sql` file in the following location:

```
./gcd_docker/data/gcd/
```

## Python Scripts

There are a collection of scripts in the `python` directory - mainly for examples. The `cbdb` folder contains a few classes for connecting to and retrieving data from the GCD database. Below is an example of how to run some of the scripts from the `gcd-python` container. Have a look at the source code to further understand the scripts and how to use/modify them.

```
docker exec gcd-python python gcd_multi_barcode_lookup.py
docker exec gcd-python python gcd_multi_issue_id_lookup.py
docker exec gcd-python python gcd_series_issues_lookup.py
docker exec gcd-python python gcd_dump_publisher_data.py
docker exec gcd-python python gcd_test_load_all_into_models.py
```

### gcd_dump_publisher_data.py

- Query database for publishers
- Output JSON file mapping ID to name

### gcd_multi_barcode_lookup.py

- Read in `example_barcodes.txt` file
- For each barcode, lookup the barcode and return all matches
- Print output in nice format

### gcd_multi_issue_id_lookup.py

- Read in `example_issues.txt` file
- For each issue ID, lookup and return the single matching issue
- Print output in nice format

### gcd_series_issues_lookup.py

- Read in `example_series_ids.txt` file
- For each series, lookup all Cover A issues
- Print output in nice format

### gcd_models.py

Note that these were manually generated using the following method:

```
# View table in MySQL and copy to file
DESCRIBE gcd_issue;
# Split the file and print needed columns
cat issue.txt | awk -F"|" '{print $2":"$3"="$6}'
# Columns are name, type, default
# Use find/replace to make changes to Python types/syntax
# Update Optional (nullable) manually
```

## Migration

Migration is a set of database models and scripts to transform the GCD data into something that I find more useful. The general steps are:

- Download new GCD database dump file
- Move un-compressed database dump file to `./data/gcd` directory
- Update `GCD_DUMP_DATE_LAST` and `GCD_DUMP_DATE_CURR` to new values
- Build GCD Docker environment using `make gcd_build`
- Run migration script as documented below

To perform a full migration:

```
docker exec gcd-python python gcd_migrate_full.py > data/tgd/migration_2023-06-01.sql
```

To perform a partial migration:

```
docker exec gcd-python python gcd_migrate_partial.py > data/tgd/migration_2023-07-01.sql
```

Check for any errors:

```
grep "^Error" data/tgd/migration_2023-06-01.sql
```

Remove error line from file:

```
awk '!/^Error/' data/tgd/migration_2023-06-01.sql
```

## Performance

The current implementation is not tweaked for performance. It has been designed to be flexible, rather than performant. Unless you are crunching lots of data, this shouldn't be a problem. Initial load of the entire GCD takes about 45GB storage, almost 1GB RAM for the dump import, and takes approximately 45 minutes (depending on your system).

The initial database load time is very slow. The GCD MySQL dump is ~2GB, and takes about 45 minutes to import on my laptop. This is a one-time import if you keep the Docker volume. However, if you want faster load times, consider extracting the `gcd_issues`, `gcd_series` and `gcd_publishers` tables, and only importing them. Depending on what you are doing, these three tables are usually sufficient - lookup issue, series and publisher metadata. These three tables are about 500MB, so the load time is much faster. To load in just these files, use the following commands to extract the tables, then **only put those sql files** into the `gcd_data` folder.


```
echo -e 'SET FOREIGN_KEY_CHECKS=0;\n' > data/gcd/issues.sql
cat ~/Downloads/2023-06-01.sql | sed -n -e '/DROP TABLE.*`gcd_issue`/,/UNLOCK TABLES/p' >> data/gcd/issues.sql
```

```
echo -e 'SET FOREIGN_KEY_CHECKS=0;\n' > data/gcd/series.sql
cat ~/Downloads/2023-06-01.sql | sed -n -e '/DROP TABLE.*`gcd_series`/,/UNLOCK TABLES/p' >> data/gcd/series.sql
```

```
echo -e 'SET FOREIGN_KEY_CHECKS=0;\n' > data/gcd/publishers.sql
cat ~/Downloads/2023-06-01.sql | sed -n -e '/DROP TABLE.*`gcd_publisher`/,/UNLOCK TABLES/p' >> data/gcd/publishers.sql
```

## GCD DB Table Structure

Some notes on the SQL database structure in the GCD project.

### All Tables

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

### Issue Table

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

### Series Tables

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

### Publisher Tables

Represents a comic book publisher. For example, Marvel.

```
mysql> describe gcd_publisher;
+------------------------------+--------------+------+-----+---------------------+----------------+
| Field                        | Type         | Null | Key | Default             | Extra          |
+------------------------------+--------------+------+-----+---------------------+----------------+
| id                           | int          | NO   | PRI | NULL                | auto_increment |
| name                         | varchar(255) | NO   | MUL | NULL                |                |
| country_id                   | int          | NO   | MUL | NULL                |                |
| year_began                   | int          | YES  | MUL | NULL                |                |
| year_ended                   | int          | YES  |     | NULL                |                |
| notes                        | longtext     | NO   |     | NULL                |                |
| url                          | varchar(255) | NO   |     | NULL                |                |
| brand_count                  | int          | NO   | MUL | 0                   |                |
| indicia_publisher_count      | int          | NO   | MUL | 0                   |                |
| series_count                 | int          | NO   |     | 0                   |                |
| created                      | datetime     | NO   |     | 1901-01-01 00:00:00 |                |
| modified                     | datetime     | NO   | MUL | 1901-01-01 00:00:00 |                |
| issue_count                  | int          | NO   |     | 0                   |                |
| deleted                      | tinyint(1)   | NO   | MUL | 0                   |                |
| year_began_uncertain         | tinyint(1)   | NO   | MUL | 0                   |                |
| year_ended_uncertain         | tinyint(1)   | NO   | MUL | 0                   |                |
| year_overall_began           | int          | YES  | MUL | NULL                |                |
| year_overall_began_uncertain | tinyint(1)   | NO   | MUL | NULL                |                |
| year_overall_ended           | int          | YES  |     | NULL                |                |
| year_overall_ended_uncertain | tinyint(1)   | NO   | MUL | NULL                |                |
+------------------------------+--------------+------+-----+---------------------+----------------+
```

### Example Queries

Lookup a comic issue with a specific barcode (including supplementary 2-5 digit code):

```
SELECT * FROM gcd_issue WHERE barcode = '75960608629004011';
```

Lookup a comic series using a specific `series_id` (found in the previous example):

```
SELECT * FROM gcd_series WHERE id = '110055';
```
