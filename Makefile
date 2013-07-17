lint:
	pep8 *.py app/*.py
	pyflakes *.py app/*.py
	grunt jshint

test:
	python app/tests.py -v

widget:
	python app/create_widget.py $(NAME)

run-job:
	python app/jobs.py $(NAME)

google-api-auth:
	python app/google-api.py
