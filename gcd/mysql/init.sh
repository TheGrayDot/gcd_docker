#!/bin/bash


echo "[*] init.sh"

echo "[*] Loading GCD database dump..."
mysql -u root -p$MYSQL_ROOT_PASSWORD gcd < "/data/gcd/$GCD_DUMP_DATE_CURR.sql"

echo "[*] Running database indexing..."
mysql -u root -p$MYSQL_ROOT_PASSWORD gcd < /data/gcd/zindex.sql

# Touch file so Docker compose heathcheck passes
echo "[*] Making service healthy..."
touch /var/lib/mysql/healthy
