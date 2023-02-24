# gcd_docker

A simple Docker Compose environment for the [Grand Comic Database (GCD)](https://www.comics.org/) with a Python environment and scripts for interacting with the database.

## Project Overview

- Uses Docker to provision containers to load and process GCD data
- MySQL container to auto load the GCD data
- MySQL container uses a volume for data storage so data is persistent
- Python container to run simple programs to query database
- Python app folder is mounted as a volume so you can edit scripts without rebuilding

## QuickStart

- Make sure you have the following installed:
    - Docker
    - Docker Compose plugin
- Clone the repo
    - `git clone https://github.com/TheGrayDot/gcd_docker.git && cd ./gcd_docker`
- Copy a GCD MySQL dump to the `gcd_data` folder
    - `cp ~/Downloads/current.zip ./gcd_data && unzip ./gcd_data/current.zip`
- Start Docker environment
    - `make run`
    - OR
    - `docker compose up --build`
- Run a Python scipt in the Docker container to lookup a barcode
    - `docker exec gcd_python python run_multi_barcode_lookup.py`

## Project Requirements

- Docker
- Docker Compose plugin

## Python Scripts

The scripts provided are mainly for examples.

### run_fetch_all_issues_in_series.py

- Read in `example_series_ids.txt` file
- For each series, lookup all Cover A issues
- Print output in nice format

### run_multi_barcode_lookup.py

- Read in `example_barcodes.txt` file
- For each barcode, lookup the barcode and return all matches
- Print output in nice format

### run_multi_gcd_issue_lookup.py

- Read in `example_issues.txt` file
- For each issue ID, lookup and return the single matching issue
- Print output in nice format

## Performance

The current implementation is not tweaked for performance. It has been designed to be flexible, rather than performant. Unless you are crunching lots of data, this shouldn't be a problem.

The initial database load time is very slow. The GCD MySQL dump is ~2GB, and takes about 45 minutes to import on my laptop. This is a one-time import if you keep the Docker volume. However, if you want faster load times, consider extracting the `gcd_issues` and `gcd_series` tables, and only importing them. Depending on what you are doing, these two tables are usually sufficient - lookup issue and series metadata. These two tables are about 400MB, so the load time is much faster. To load in just these files, use the following commands to extract the tables, then **only put those sql files** into the `gcd_data` folder.


```
echo -e 'SET FOREIGN_KEY_CHECKS=0;\n' > gcd_data/gcd_series.sql
cat 2022-04-01.sql | sed -n -e '/DROP TABLE.*`gcd_series`/,/UNLOCK TABLES/p' >> gcd_data/gcd_series.sql
```

```
echo -e 'SET FOREIGN_KEY_CHECKS=0;\n' > gcd_data/gcd_issue.sql
cat 2022-04-01.sql | sed -n -e '/DROP TABLE.*`gcd_issue`/,/UNLOCK TABLES/p' >> gcd_data/gcd_issue.sql
```
