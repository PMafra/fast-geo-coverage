#!/bin/bash

# Check if all required environment variables are set
if [[ -z "$APP_DB_USER" || -z "$APP_DB_PASSWORD" || -z "$APP_DB_HOST" || -z "$APP_DB_PORT" || -z "$APP_DB_NAME" ]]; then
  echo "One or more required environment variables are not set."
  echo "Make sure APP_DB_USER, APP_DB_PASSWORD, APP_DB_HOST, APP_DB_PORT, and APP_DB_NAME are set."
  exit 1
fi

# Create the database using the provided environment variables
echo "Creating database '$APP_DB_NAME' on '$APP_DB_HOST:$APP_DB_PORT'..."

mysql -u"$APP_DB_USER" -p"$APP_DB_PASSWORD" -h "$APP_DB_HOST" -P "$APP_DB_PORT" -e "CREATE DATABASE IF NOT EXISTS \`$APP_DB_NAME\`;"

if [[ $? -eq 0 ]]; then
  echo "Database '$APP_DB_NAME' created or already exists."
else
  echo "Failed to create database '$APP_DB_NAME'. Please check your connection details and try again."
  exit 1
fi
