# add some others
export DJANGO_SETTINGS_MODULE=app.settings
python manage.py makemigrations app
python manage.py migrate app
python manage.py runserver 0.0.0.0:80
