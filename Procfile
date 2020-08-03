web: gunicorn URLShortenerDjango.wsgi --log-file -
python manage.py collectstatic --noinput
python manage.py makemigrations main
python manage.py migrate