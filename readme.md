# Videoflix Backend

## Overview

Videoflix is a backend service for a video streaming platform. This project is built using Django and it provides various features such as user registration, password reset, video management, and more.

## Features

- **User Management**: Registration, login, and password reset functionalities.
- **Video Management**: Upload, manage, and stream videos.
- **Email Notifications**: Send emails for registration and password reset.
- **Redis Queue**: Background task processing using Redis.
- **REST API**: Expose endpoints for frontend interaction.
- **Admin Interface**: Manage users, videos, and other data through Django's admin interface.

## Prerequisites
- Python 3.12
- PostgreSQL Database

## Setup & Starting the App
Open CMD at Root Directory level and run
1. **Create a virtual environment with:** `python -m venv env`
2. **Start the virtual environment with:** `"env/Scripts/activate"` or `.\\env\Scripts\activate`
3. **Install dependencies with:** `pip install -r requirements.txt`
4. **Set Global Environment Variables in '.env' file:** Rename the document **.env_example** to **.env** and adjust its variable values:
   
```
//.env
EMAIL_HOST_USER = 'my email'
EMAIL_HOST_PASSWORD = 'my_email_password'
DJANGO_DEBUG=True
DEV_HOST='http://localhost'
PROD_HOST='http://mysite.com'
FRONTEND_HOST='localhost:4200'
```

5. **Setup PostgreSQL DB:** Create a PostgreSQL DB by the name **"videoflix_db"**
6. **Adjust settings.py to connect to your PostgreSQL DB like so:**
   ```
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'videoflix_db',
           'USER': 'postgres',
           'PASSWORD': 'MySuper1234Pa$$word',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
7. **Create your Data Base by running:** `python manage.py makemigrations` AND `python manage.py migrate`
8. **Create SuperUser for Django Admin:** `python manage.py createsuperuser`
9.  Run `start_all.bat` to start the Django Backend in one cli and Redis + the RQ Worker in another cli.
10.  


This will 
### Local Development

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/videoflix-bknd.git
    cd videoflix-bknd
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

6. **Start the development server**:
    ```sh
    python manage.py runserver
    ```

7. **Start the Redis worker**:
    ```sh
    ./start_rq_worker.sh
    ```

8. **Access the application**:
    - The application will be available at `http://localhost:8000`
    - The admin interface will be available at `http://localhost:8000/admin`

## Configuration

### Environment Variables

Create a `.env` file in the root directory and add the following variables:

```
//.env
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
FRONTEND_HOST=http://localhost:4200
```

## PostgreSQL setup
Start you WSL Client on your windows mashine:
`source env_lin/bin/activate`

Update **apt** Installation:
`sudo apt update` and `sudo apt upgrade`

Install postgresql and postgresql-contrib
`sudo apt install postgresql postgresql-contrib`

Check the postgreSQL status on your Linux mashine:
`sudo service postgresql status` //check stauts
`sudo service postgresql start` //start postgresql if needed
`sudo service postgresql stop` //stop postgresql if needed

*IMPORTANT:* *Switch to the postgres user. User sudo, because you don't want to set the password* *(postgreSQL is by default locked)*
`sudo -i -u postgres`

*Die PostgreSQL Datenbank läuft nun im Hintergrund auf deiner Linux Mashine als Dienst. Du kannst mit `dpkg -l | grep postgresql` alle PostgreSQL Installationen prüfen.

Exit with `exit`

### Install your PostgreSQL DB
Open the postgresql client:
`psql`

Create your Database like so:
 ``` 
CREATE DATABASE videoflix;
CREATE USER Alex WITH PASSWORD 'Test123';
ALTER ROLE Alex SET client_encoding TO 'utf8';
ALTER ROLE Alex SET default_transaction_isolation TO 'read committed';
ALTER ROLE Alex SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE videoflix TO Alex;
```

List your databases:
`\l`

Exit the PostgreSQL terminal:
`\q`

Remember! PostgreSQL must be running on you mashine:
`sudo service postgresql start`

You have to be the "postgres" user:
`sudo -i -u postgres`

The PostgreSQL Client must be running:
`psql` 

Then you can list your db's with `\l`

### Connect Django with PostgreSQL
Install an adapter that helps to connect:
`pip install psycopg2-binary` 

Open via WSL you Django settings.py and add the database configuratin:
```
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'videoflix',
		'USER': 'Alex',
		'PASSWORD': 'Test123',
		'HOST': 'localhost',
		'PORT': '',
	}
}
```

