#!/usr/bin/env bash

echo "Running docker-entrypoint initialization script"

# run migrations on sqlite database
alembic upgrade head

# create, if needed, the admin user
voilib-management --create-admin

# run the CMD passed as command-line arguments
exec "$@"
