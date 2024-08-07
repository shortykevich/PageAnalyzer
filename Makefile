PORT ?= 8000

install:
	poetry install

build:
	./build.sh

dev:
	poetry run flask --app page_analyzer:app run --port $(PORT)


dev-debug:
	poetry run flask --app page_analyzer:app --debug run --port $(PORT)


start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


lint:
	poetry run flake8


test:
	poetry run coverage run -m pytest


coverage:
	poetry run coverage report -m
