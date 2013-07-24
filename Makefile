all: lint test

lint-py:
	pep8 *.py app/*.py
	pyflakes *.py app/*.py

lint-js:
	grunt jshint

lint: lint-py lint-js

test:
	python app/tests.py

clean:
	rm -f *.pyc app/*.pyc
	rm -fr bower_components/
	rm -fr app/static/.webassets-cache/
	rm -fr app/static/assets/

release: clean lint-py test
release:
	grunt

widget:
	python app/create_widget.py $(NAME)

run-job:
	python app/jobs.py $(NAME)

google-api-auth:
	python app/google_api_auth.py
