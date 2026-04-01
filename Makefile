APP_ROOT := jarvis

all: clean lint test

lint-py:
	uv run ruff check

lint-js:
ifdef CI
	npm install -g jshint
	git ls-files '*.js' | xargs jshint
endif

lint: lint-py lint-js

test:
	env TZ=UTC uv run $(APP_ROOT)/tests.py

clean:
	rm -rf $(APP_ROOT)/**/*.pyc $(APP_ROOT)/static/.webassets-cache/ $(APP_ROOT)/static/gen/

widget:
	uv run $(APP_ROOT)/util/create_widget.py $(NAME)

dashboard:
	uv run $(APP_ROOT)/util/create_dashboard.py $(NAME)

debug:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	uv run flask --app $(APP_ROOT)/app --debug run

run:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	uv run flask --app $(APP_ROOT)/app run

run-job:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	uv run $(APP_ROOT)/run_job.py $(NAME)

google-api-auth:
ifndef JARVIS_SETTINGS
	$(error JARVIS_SETTINGS must be set)
endif
	uv run $(APP_ROOT)/util/google_api_auth.py
