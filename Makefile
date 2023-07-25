PYTHON ?= python3
BLACK ?= $(PYTHON) -m black --quiet --check
PIP ?= $(PYTHON) -m pip
VENV ?= $(PYTHON) -m venv
APP_ROOT := jarvis

all: clean lint test

lint-py: black

black:
	git ls-files '*.py' | xargs $(BLACK)

lint-js:
ifdef CI
	git ls-files '*.js' | xargs jshint
endif

lint: lint-py lint-js

test:
	env TZ=UTC $(PYTHON) $(APP_ROOT)/tests.py

clean:
	rm -rf $(APP_ROOT)/**/*.pyc $(APP_ROOT)/static/.webassets-cache/ $(APP_ROOT)/static/gen/

widget:
	$(PYTHON) $(APP_ROOT)/util/create_widget.py $(NAME)

dashboard:
	$(PYTHON) $(APP_ROOT)/util/create_dashboard.py $(NAME)

debug:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	FLASK_APP=$(APP_ROOT)/app FLASK_ENV=development flask run

run:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	FLASK_APP=$(APP_ROOT)/app flask run

run-job:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	$(PYTHON) $(APP_ROOT)/run_job.py $(NAME)

google-api-auth:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	$(PYTHON) $(APP_ROOT)/util/google_api_auth.py

list-outdated-deps:
	$(PIP) list --outdated --not-required

venv:
	$(VENV) venv

install-requirements:
	$(PIP) install -r requirements-build.txt
	$(PIP) install -r requirements.txt
ifdef CI
	npm install -g jshint
endif
