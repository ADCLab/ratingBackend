#!/bin/bash

# Define environment variables (you can override these variables by exporting them)
HOSTNAME=${MYSQL_HOSTNAME:-localhost}           # Default hostname: localhost
USERNAME=${MYSQL_USER:-root}                # Default username: root
PASSWORD=${MYSQL_PASSWORD:-password123}         # Default password
DATABASE_NAME=${MYSQL_DATABASE:-mydb}      # Default database name: mydb
PORT=${PORT:-3306}                        # Default port number: 3306

# Hardcoded SQL script path
SCRIPT_PATH="init.sql"                    # Hardcoded path to the SQL script

# Check if required environment variables are properly set
if [ -z "$HOSTNAME" ] || [ -z "$USERNAME" ] || [ -z "$PASSWORD" ] || [ -z "$DATABASE_NAME" ] || [ -z "$PORT" ]; then
    echo "Error: One or more required variables are missing!"
    echo "Make sure the following variables are set:"
    echo "  - HOSTNAME"
    echo "  - USERNAME"
    echo "  - PASSWORD"
    echo "  - DATABASE_NAME"
    echo "  - PORT"
    exit 1
fi

# Check if the hardcoded SQL script file exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: SQL script file '$SCRIPT_PATH' not found!"
    exit 1
fi

# Run the MySQL command using the environment variables, including port
mysql -h "$HOSTNAME" -P "$PORT" -u "$USERNAME" -p"$PASSWORD" "$DATABASE_NAME" < "$SCRIPT_PATH"

# Check for errors in execution
if [ $? -eq 0 ]; then
    echo "SQL script executed successfully!"
else
    echo "Failed to execute SQL script."
    exit 1
fi

