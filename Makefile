run:
	docker compose up --build

clean:
	docker compose down; \
	docker image rm mysql:8.0; \
	docker image rm python:3.9-slim-bullseye;

remove_volume:
	sudo rm -rf ./volumes/mysql
