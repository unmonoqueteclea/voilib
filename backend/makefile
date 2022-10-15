# Copyright (c) 2022-2023 Pablo González Carrizo
# All rights reserved.
include .env

help:
	@echo "📻 voilib - podcast search engine [backend python project]  "
	@echo "                                                            "
	@echo "Available targets:                                          "
	@echo "    - help: show this message                               "
	@echo "    - start: run the back-end locally                       "
	@echo "    - gen-migrations: generate new migrations               "
	@echo "    - migrate: apply all migrations                         "

start:
	uvicorn src.voilib.main:app --reload --host 0.0.0.0 --port 8080


gen-migrations:
	@read -p "Enter migration message:" msg; \
	alembic revision --autogenerate -m "$$msg"

migrate:
	alembic upgrade head
