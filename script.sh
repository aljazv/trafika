find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

rm db.sqlite3

python3 manage.py makemigrations
python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminadmin', first_name='Skrbnik')" | python3 manage.py shell
