# add some others
export DJANGO_SETTINGS_MODULE=app.settings
python manage.py migrate
python manage.py runserver localhost:80
