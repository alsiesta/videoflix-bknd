#!/bin/bash

echo "Updating package list..."
sudo apt update

echo "Upgrading installed packages..."
sudo apt upgrade -y

echo "Installing PostgreSQL and contrib package..."
sudo apt install -y postgresql postgresql-contrib

echo "Setting PostgreSQL default user password..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'Test123';"

echo "Starting PostgreSQL service..."
sudo service postgresql start

echo "Creating PostgreSQL database 'videoflix_db'..."
sudo -u postgres CREATE DATABASE videoflix_db

echo "Listing PostgreSQL databases..."
sudo "\l"
\q

echo "Creating virtual environment..."
# Create virtual environment
python3 -m venv myvenv

echo "Activating virtual environment..."
# Activate virtual environment
source myvenv/bin/activate

echo "Installing requirements..."
# Install requirements
pip install -r requirements.txt

echo "Starting RQ worker..."
# While Redis is automatically in Ubuntu the rq worker needs to be started manually
python3 manage.py rqworker default

echo "Create database tables..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Creating superuser..."
expect << EOF
spawn python3 manage.py createsuperuser --username Alex --email ""
expect "Password:"
send "12\r"
expect "Password (again):"
send "12\r"
expect "Bypass password validation and create user anyway? (y/N)"
send "y\r"
expect eof
EOF

echo "All tasks completed."