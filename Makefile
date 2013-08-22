all: lint test

lint-py:
	flake8 --max-complexity=10 *.py app/*.py app/jobs/*.py support/*.py

lint-js:
	grunt jshint

lint: lint-py lint-js

test:
	python app/tests.py

clean:
	rm -f *.pyc app/*.pyc app/jobs/*.pyc support/*.pyc
	rm -fr app/static/.webassets-cache/
	rm -fr app/static/assets/

release: clean lint-py test
release:
	grunt

widget:
	python support/create_widget.py $(NAME)

dashboard:
	python support/create_dashboard.py $(NAME)

debug:
	python app/run.py debug

run:
	python app/run.py

run-job:
	python app/run.py job $(NAME)

google-api-auth:
	python support/google_api_auth.py
