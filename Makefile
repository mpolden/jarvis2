APP_ROOT := jarvis

all: clean lint test

lint-py:
	find . -name '*.py' | xargs flake8 --max-complexity=8

lint-js:
ifdef TRAVIS
	find . -name '*.js' | xargs jshint
else
	@echo "lint-js: Skipping, not running on Travis"
endif

lint: lint-py lint-js

test:
	python $(APP_ROOT)/tests.py

clean:
	find . -name '*.pyc' -delete
	rm -rf $(APP_ROOT)/static/.webassets-cache/ $(APP_ROOT)/static/gen/

widget:
	python $(APP_ROOT)/util/create_widget.py $(NAME)

dashboard:
	python $(APP_ROOT)/util/create_dashboard.py $(NAME)

debug:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	python $(APP_ROOT)/run.py --debug

run:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	python $(APP_ROOT)/run.py

run-job:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	python $(APP_ROOT)/run.py --job $(NAME)

google-api-auth:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	python $(APP_ROOT)/util/google_api_auth.py
