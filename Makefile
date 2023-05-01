tailwind: 
	npx tailwindcss -i ./pit_parser/static/src/input.css -o ./pit_parser/static/src/output.css --watch
run: 
	python ./pit_parser/manage.py runserver
migrate:
	python ./pit_parser/manage.py migrate
migrations:
	python ./pit_parser/manage.py makemigrations
