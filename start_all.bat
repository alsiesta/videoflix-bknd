@echo off
start cmd /k "python manage.py runserver"
wsl bash -c "./start_rq_worker.sh"
