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

copy-resources:
	mkdir -p \
		app/static/css/gridster \
		app/static/css/normalize-css \
		app/static/css/rickshaw \
		app/static/js/angular \
		app/static/js/angular-truncate \
		app/static/js/d3 \
		app/static/js/gauge.js \
		app/static/js/gridster \
		app/static/js/jquery \
		app/static/js/moment \
		app/static/js/rickshaw
	cp -p bower_components/angular/angular.min.js app/static/js/angular/
	cp -p bower_components/angular-truncate/dist/angular-truncate.min.js \
		app/static/js/angular-truncate/
	cp -p bower_components/d3/d3.min.js app/static/js/d3/
	cp -p bower_components/gauge.js/dist/gauge.min.js app/static/js/gauge.js/
	cp -p bower_components/gridster/dist/jquery.gridster.min.css \
		app/static/css/gridster/
	cp -p bower_components/gridster/dist/jquery.gridster.min.js \
		app/static/js/gridster/
	cp -p bower_components/jquery/jquery.min.js app/static/js/jquery/
	cp -p bower_components/moment/min/moment.min.js app/static/js/moment/
	cp -p bower_components/moment/min/lang/nb.js app/static/js/moment/
	cp -p bower_components/normalize-css/normalize.css \
		app/static/css/normalize-css/
	cp -p bower_components/rickshaw/rickshaw.min.css app/static/css/rickshaw/
	cp -p bower_components/rickshaw/rickshaw.min.js app/static/js/rickshaw/


release: clean lint-py test copy-resources
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
