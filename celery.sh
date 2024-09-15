export DJANGO_SETTINGS_MODULE="core.settings"
python -m celery -A apps.tasks worker -l info --purge -B
