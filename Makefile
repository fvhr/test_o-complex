mig:
	@cd weather_forecast && python manage.py makemigrations
	@cd weather_forecast && python manage.py migrate

check: test
	@black .
	@flake8 .

test:
	@cd weather_forecast && python manage.py test

run:
	@cd weather_forecast && python manage.py runserver

su:
	@cd weather_forecast && python manage.py createsuperuser

ir:
	@pip install -r requirements/dev.txt

loc-m:
	@cd weather_forecast && django-admin makemessages -l ru -l en

loc-c:
	@cd weather_forecast && django-admin compilemessages

dump:
	@cd weather_forecast && python -Xutf8 manage.py dumpdata geo --format json --indent 4 -o fixtures/data.json

load:
	@cd weather_forecast && python -Xutf8 manage.py loaddata fixtures/data.json
