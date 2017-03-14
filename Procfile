web: gunicorn maquette.wsgi:application --pythonpath ./maquette --log-file - --access-logfile -
web: python maquette/manage.py collectstatic --noinput; bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT maquette/settings.py 
