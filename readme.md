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
- *"WSL active on you Windows Mashine"* or you work on Linux

## Setup
Rename the '.env_example' file to simply '.env'
For review purposes by the "Developer Akademie" I left my personal credentials in this file like so: 

```
//.env
EMAIL_HOST_USER = 'schoenfeldalexander@googlemail.com'
EMAIL_HOST_PASSWORD = 'ktmw rklg aurw fder'
DJANGO_DEBUG=True
DEV_HOST='http://localhost'
PROD_HOST='http://mysite.com'
FRONTEND_HOST='localhost:4200'
```

## Setup & Starting the App
Open the WSL (Ubuntu or Bash) shell at Root Directory level.

Then either run `source start.sh` or `./start.sh`.
(The first command keeps the virtual environment visible in the terminal during the installation process. The second runs the installation in a subshell. The results are identical.)

**IMPORTANT:** 
- During installation you have to submit a name for the PostgreSQL database. Name it **"videoflix_db"** 
- During installation you also have to give the superuser a **name, email and password**.

That's it.

### What happens during installation:
1. **Upgrading apt package manager**
2. **Installing all required packages like:** postgresql, postgresql-contrib, expect, python3-venv
3. **Starting the PostgreSQL service in your WSL**
4. **Setting the PostgreSQL default user password to "Test123"**
5. **Creation of PostgreSQL database**
   1. When prompted to give the db a name type: **"videoflix_db"**
6. **Listing the PostgreSQL databases for controlling**
7. **Creation of the virtual environment "myvenv"**
8. **Starting the virtual environment**
9. **Installation of all dependencies in Virtual Env.**
10. **Migrating the Django DB to PostgreSQL DB**
11. **Starting Redis Que Worker in a subshell**
    1.  this will run the Video Formating Processes in parallel and
    2.  it runs the Cache
12. **Checking if port 8000 is available**
13. **Starting the Django Backend-Server on port 8000**
14. If you started the script with "source start.sh" the Django Admin UI will open in your browser under: http://127.0.0.1:8000/admin


### Note:
In the settings.py file of the Django App, the Database Settings should look like so now:
   ```
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'videoflix_db',
           'USER': 'postgres',
           'PASSWORD': 'Test123',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }

   ```



