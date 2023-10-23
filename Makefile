include .env

gcd_run:
	docker compose --file docker-compose_gcd.yml up

gcd_build:
	docker compose --file docker-compose_gcd.yml up --build

gcd_clean:
	docker compose --file docker-compose_gcd.yml down; \
	docker image rm gcd-mysql:${GCD_DUMP_DATE_CURR}; \
	docker image rm gcd-python:${GCD_DUMP_DATE_CURR};

gcd_remove_volumes:
	sudo rm -rf ./data/volumes/gcd_mysql*

tgd_run:
	docker compose --file docker-compose_tgd.yml up

tgd_build:
	docker compose --file docker-compose_tgd.yml up --build

tgd_clean:
	docker compose --file docker-compose_tgd.yml down; \
	docker image rm tgd-mysql:${TGD_DUMP_DATE_CURR}; \
	docker image rm tgd-python:${TGD_DUMP_DATE_CURR};

tgd_remove_volumes:
	sudo rm -rf ./data/volumes/tgd_mysql*

python_lint:
	python3 -m venv ./python/venv; \
	.  ./python/venv/bin/activate && \
	pip3 install -r ./python/requirements.txt && \
	black ./python
