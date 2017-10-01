APP_ROOT := jarvis

all: clean lint test

lint-py:
	flake8 --max-complexity=8 $(APP_ROOT)/*.py $(APP_ROOT)/jobs/*.py support/*.py

lint-js:
ifdef TRAVIS
	jshint $(APP_ROOT)/static/*.js $(APP_ROOT)/static/widgets/*/*.js
else
	@echo "lint-js: Skipping, not running on Travis"
endif

lint: lint-py lint-js

test:
	python $(APP_ROOT)/tests.py

clean:
	rm -rf *.pyc $(APP_ROOT)/*.pyc $(APP_ROOT)/jobs/*.pyc support/*.pyc \
$(APP_ROOT)/static/.webassets-cache/ $(APP_ROOT)/static/gen/

widget:
	python support/create_widget.py $(NAME)

dashboard:
	python support/create_dashboard.py $(NAME)

debug:
	python $(APP_ROOT)/run.py --debug

run:
	python $(APP_ROOT)/run.py

run-job:
	python $(APP_ROOT)/run.py --job $(NAME)

google-api-auth:
	python support/google_api_auth.py
