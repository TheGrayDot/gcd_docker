gcd_run:
	docker compose -f docker-compose_gcd.yml up

gcd_build:
	docker compose -f docker-compose_gcd.yml up --build

gcd_clean:
	docker compose -f docker-compose_gcd.yml down; \
	docker image rm mysql:8.0; \
	docker image rm python:3.9-slim-bullseye;

gcd_remove_volume:
	sudo rm -rf ./volumes/mysql

tgd_run:
	docker compose -f docker-compose_tgd.yml up

tgd_build:
	docker compose -f docker-compose_tgd.yml up --build
