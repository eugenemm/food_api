#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER food_backend_db_user  WITH PASSWORD '12345678';
    CREATE DATABASE food_db  OWNER 'food_backend_db_user';
EOSQL
