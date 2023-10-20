#!/usr/bin/env bash

echo "Voilib initialization..."
alembic upgrade head  # run migrations on sqlite database
voilib-management --create-admin # create, if needed, the admin user
exec "$@" # run the CMD passed as command-line arguments
