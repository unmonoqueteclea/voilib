help:
	@echo "Voilib Infrastructure                                      "
	@echo "\nAvailable targets for development: "
	@echo " - make dev-build: build Docker images in development mode        "
	@echo " - make dev-run: start all services in development mode    "
	@echo "\nAvailable targets for production: "
	@echo " - make prod-build: build Docker images in production mode        "
	@echo " - make prod-run: start all services in production mode    "


test-env-dev:
	@echo "checking if .env.dev exists in ./development, you should have created it"
	test -s ./development/.env.dev

test-env-prod:
	@echo "checking if .env.prod exists in ./production, you should have created it"
	test -s ./production/.env.prod

dev-build: test-env-dev
	cd development/ && docker compose --env-file=.env.dev build

dev-run: test-env-dev
	cd development/ && docker compose --env-file=.env.dev up

prod-build: test-env-prod
	cd production/ && docker compose --env-file=.env.prod build

prod-run: test-env-prod
	cd production/ && docker compose --env-file=.env.prod up
