collectstatic: 
	python ./pit_parser/manage.py collectstatic
run: 
	python ./pit_parser/manage.py runserver
migrate:
	python ./pit_parser/manage.py migrate
migrations:
	python ./pit_parser/manage.py makemigrations
shell:
	python ./pit_parser/manage.py shell
web: 
	npx tailwindcss -i ./pit_parser/static/src/input.css -o ./pit_parser/static/src/output.css --watch