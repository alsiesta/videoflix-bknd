#!/bin/bash

set -e

echo "----------- Updating package list..."
sudo apt update
sudo apt upgrade -y

echo "----------- Installing required packages..."
sudo apt install -y postgresql postgresql-contrib expect python3-venv

echo "----------- Starting PostgreSQL service..."
sudo service postgresql start

echo "----------- Setting PostgreSQL default user password..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'Test123';"

#echo "----------- Creating PostgreSQL database 'videoflix_db2'..."
#sudo -u postgres psql -c "CREATE DATABASE videoflix_db2;"

# Prompt the user to enter a database name
read -p "Please enter the name of the PostgreSQL database to create: " dbname

echo "----------- Creating PostgreSQL database '$dbname'..."
sudo -u postgres psql -c "CREATE DATABASE $dbname;"

echo "----------- Listing PostgreSQL databases..."
sudo -u postgres psql -c "\l"

echo "----------- Creating virtual environment..."
python3 -m venv myvenv

if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Wait until the activation script exists
while [ ! -f "myvenv/bin/activate" ]; do
    sleep 1
done

echo "----------- Activating virtual environment..."
source myvenv/bin/activate


if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment not activated."
    exit 1
else
    echo "Virtual environment activated: $VIRTUAL_ENV"
fi

echo "Using pip from: $(which pip)"
echo "Using python from: $(which python)"

echo "----------- Installing requirements..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "----------- Creating database tables..."
python manage.py makemigrations
python manage.py migrate

echo "----------- Creating superuser..."
echo "----------- Please create a superuser for Django admin interface"
echo "----------- Add Name, Email, and Password when prompted"
python manage.py createsuperuser

echo "----------- Starting RQ worker in a separate shell..."
nohup bash -c "python manage.py rqworker default" > rqworker.log 2>&1 &

echo "----------- Checking if port 8000 is in use..."
if lsof -i:8000; then
  echo "----------- Port 8000 is in use. Killing the process..."
  fuser -k 8000/tcp
fi

echo "----------- Starting Django development server..."
python manage.py runserver &

echo "----------- Waiting for Django development server to start..."
while ! nc -z localhost 8000; do
  sleep 1
done

echo "----------- Opening browser to Django admin interface..."
explorer.exe "http://127.0.0.1:8000/admin" &

echo "All tasks completed."