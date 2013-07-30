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

copy-resources:
	bower install
	mkdir -p app/static/css/gridster app/static/css/normalize-css \
		app/static/css/rickshaw app/static/js/angular \
		app/static/js/angular-truncate app/static/js/app app/static/js/d3 \
		app/static/js/gridster app/static/js/jquery app/static/js/jquery-knob \
		app/static/js/moment app/static/js/rickshaw
	cp -p bower_components/angular/angular.min.js app/static/js/angular/
	cp -p bower_components/angular-truncate/dist/angular-truncate.min.js \
		app/static/js/angular-truncate/
	cp -p bower_components/d3/d3.min.js app/static/js/d3/
	cp -p bower_components/gridster/dist/jquery.gridster.css \
		app/static/css/gridster/
	cp -p bower_components/gridster/dist/jquery.gridster.min.js \
		app/static/js/gridster/
	cp -p bower_components/jquery/jquery.min.js app/static/js/jquery/
	cp -p bower_components/jquery-knob/js/jquery.knob.js \
		app/static/js/jquery-knob/
	cp -p bower_components/moment/min/moment.min.js app/static/js/moment/
	cp -p bower_components/normalize-css/normalize.css \
		app/static/css/normalize-css/
	cp -p bower_components/rickshaw/rickshaw.css app/static/css/rickshaw/
	cp -p bower_components/rickshaw/rickshaw.min.js app/static/js/rickshaw/


release: clean lint-py test copy-resources
release:
	grunt

widget:
	python app/create_widget.py $(NAME)

run-job:
	python app/jobs.py $(NAME)

google-api-auth:
	python app/google_api_auth.py
