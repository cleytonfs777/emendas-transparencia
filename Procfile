web: python manage.py migrate && python create_superuser.py && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
