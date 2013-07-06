lint:
	pep8 *.py app/*.py
	pyflakes *.py app/*.py

widget:
	@test -n "$(NAME)" || \
		(echo "NAME is not set. Use NAME=widget_name make widget" && exit 1)
	python app/create_widget.py $(NAME)
