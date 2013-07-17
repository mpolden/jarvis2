lint:
	pep8 *.py app/*.py
	pyflakes *.py app/*.py
	grunt jshint

test:
	python app/tests.py -v

widget:
	@test -n "$(NAME)" || \
		(echo "NAME is not set. Use NAME=widget_name make widget" && exit 1)
	python app/create_widget.py $(NAME)

google-api-auth:
	python app/google-api.py
