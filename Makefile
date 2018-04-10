.PHONY: tests coverage

tests:
	nosetests tests

coverage:
	nosetests --with-coverage --cover-package=hitbtcapi tests
	coverage html --include='hitbtcapi*'
