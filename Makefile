gcd_run:
	docker compose --file docker-compose_gcd.yml up

gcd_build:
	docker compose --file docker-compose_gcd.yml up --build

gcd_clean:
	docker compose --file docker-compose_gcd.yml down; \
	docker image rm mysql:8.0; \
	docker image rm python:3.9-slim-bullseye;

gcd_remove_volume:
	sudo rm -rf ./data/volumes/mysql

tgd_run:
	docker compose --file docker-compose_tgd.yml up

tgd_build:
	docker compose --file docker-compose_tgd.yml up --build
