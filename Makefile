ENV=$(VIRTUAL_ENV)
SRC_DIR=./app

lint: black . && isort . && flake8

flake8:
	$(ENV)/bin/flake8 $(SRC_DIR) > pyflakes.log || :

black:
	$(ENV)/bin/black $(SRC_DIR) > pyflakes.log || :

isort:
	$(ENV)/bin/isort . $(SRC_DIR) > pyflakes.log || :
