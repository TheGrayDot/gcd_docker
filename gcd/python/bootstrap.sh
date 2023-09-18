#!/bin/bash


pip3 install -r /python/requirements.txt

# Dump publisher data
python gcd_dump_publisher_data.py

if [ "$GCD_FULL_MIGRATION" = true ] ; then
    # Perform a full migration if requested
    python gcd_migrate_full.py > "data/migration_$GCD_DUMP_DATE_CURR.sql"
elif [ "$GCD_PARTIAL_MIGRATION" = true ] ; then
    # Perform a partial migration
    python gcd_migrate_partial.py > "data/migration_$GCD_DUMP_DATE_CURR.sql"
else
    # If do nothing, keep container up to use database
    tail -f /dev/null
fi
