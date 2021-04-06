# add some others
export DJANGO_SETTINGS_MODULE=app.settings
python manage.py makemigrations app
python manage.py migrate app
python manage.py createcachetable
if [ -f "/config/production.json" ]
then
DJANGO_SUPERUSER_USERNAME=$(cat config/production.json | jq .DJANGO_SUPERUSER_USERNAME -r)
DJANGO_SUPERUSER_EMAIL=$(cat config/production.json | jq .DJANGO_SUPERUSER_EMAIL -r)
DJANGO_SUPERUSER_PASSWORD=$(cat config/production.json | jq .DJANGO_SUPERUSER_PASSWORD -r)
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi
fi
python manage.py runserver $BIND --insecure
