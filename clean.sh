#!/bin/bash


docker-compose down
docker system prune -a -f

echo "[+] Do you wish to remove existing MySQL data?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) sudo rm -rf ./volumes/mysql; break;;
        No ) exit;;
    esac
done
