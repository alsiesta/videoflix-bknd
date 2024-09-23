# Videoflix Backend

## Overview

Videoflix is a backend service for a video streaming platform. This project is built using Django and provides various features such as user registration, password reset, video management, and more.

## Usage

## Features

- **User Management**: Registration, login, and password reset functionalities.
- **Video Management**: Upload, manage, and stream videos.
- **Email Notifications**: Send emails for registration and password reset.
- **Redis Queue**: Background task processing using Redis.
- **REST API**: Expose endpoints for frontend interaction.
- **Admin Interface**: Manage users, videos, and other data through Django's admin interface.

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- Redis

## Setup

### Using Docker

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/videoflix-bknd.git
    cd videoflix-bknd
    ```

2. **Build and run the Docker container**:
    ```sh
    docker build -t videoflix-bknd -f .devcontainer/Dockerfile .
    ```

3. **Run migrations**:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

4. **Create a superuser**:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

5. **Access the application**:
    - The application will be available at `http://localhost:8000`
    - The admin interface will be available at `http://localhost:8000/admin`

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
