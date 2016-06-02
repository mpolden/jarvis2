all: lint test

fmt:
	autopep8 --in-place app/*.py app/jobs/*.py support/*.py

flake8:
	flake8 --max-complexity=8 app/*.py app/jobs/*.py support/*.py

jshint:
	jshint app/static/*.js app/static/widgets/*/*.js

lint: flake8 jshint

test:
	python app/tests.py

clean:
	rm -f *.pyc app/*.pyc app/jobs/*.pyc support/*.pyc
	rm -fr app/static/.webassets-cache/
	rm -fr app/static/gen/

release: clean lint test

widget:
	python support/create_widget.py $(NAME)

dashboard:
	python support/create_dashboard.py $(NAME)

debug:
	python app/run.py --debug

run:
	python app/run.py

run-job:
	python app/run.py --job $(NAME)

google-api-auth:
	python support/google_api_auth.py

update-deps:
	pip install -U -r requirements-to-freeze.txt
	pip freeze | grep -vE 'argparse|wsgiref' > requirements.txt
