#!/bin/bash

echo "----------- Updating package list..."
sudo apt update

echo "----------- Upgrading installed packages..."
sudo apt upgrade -y

echo "----------- Installing PostgreSQL and contrib package..."
sudo apt install -y postgresql postgresql-contrib expect

echo "----------- Starting PostgreSQL service..."
sudo service postgresql start

echo "----------- Setting PostgreSQL default user password..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'Test123';"

echo "----------- Creating PostgreSQL database 'videoflix_db'..."
sudo -u postgres psql -c "CREATE DATABASE videoflix_db;"

echo "----------- Listing PostgreSQL databases..."
sudo -u postgres psql -c "\l"

echo "----------- Creating virtual environment..."
# Create virtual environment
python3 -m venv myvenv

echo "----------- Activating virtual environment..."
# Activate virtual environment
source myvenv/bin/activate

echo "----------- Installing requirements..."
# Install requirements
pip install -r requirements.txt

echo "----------- Create database tables..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "----------- Creating superuser..."

echo "----------- Please create a superuser for Django admin interface"
echo "----------- Add Name, Email and Password when prompted"
python3 manage.py createsuperuser

echo "----------- Starting RQ worker in a separate shell..."
# Start RQ worker in a separate shell
nohup bash -c "python3 manage.py rqworker default" > rqworker.log 2>&1 &

echo "----------- Checking if port 8000 is in use..."
if lsof -i:8000; then
  echo "----------- Port 8000 is in use. Killing the process..."
  fuser -k 8000/tcp
fi

echo "----------- Starting Django development server..."
python3 manage.py runserver &

# Wait for the server to start
echo "----------- Waiting for Django development server to start..."
while ! nc -z localhost 8000; do   
  sleep 1 # wait for 1 second before checking again
done

echo "----------- Opening browser to Django admin interface..."
# Use explorer.exe to open the browser in Windows
explorer.exe "http://127.0.0.1:8000/admin" &

echo "All tasks completed."