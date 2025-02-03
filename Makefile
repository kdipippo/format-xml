.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	python3.12 -V
	python3.12 -m site

.PHONY: install
install:          ## Install the project in dev mode.
	@echo "Don't forget to run 'make virtualenv' if you got errors."
	python3.12 -m pip install -e .[test]

## ---LINTING AND FORMATTING-------

.PHONY: format
format:           ## Format code using black & isort.
	python3.12 -m isort -l 119 format_xml/
	python3.12 -m isort -l 119 tests/
	python3.12 -m black -l 119 format_xml/
	python3.12 -m black -l 119 tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters on Python code.
	python3.12 -m flake8 format_xml/
	python3.12 -m flake8 tests/
	python3.12 -m black -l 119 --check format_xml/
	python3.12 -m black -l 119 --check tests/
	python3.12 -m mypy --ignore-missing-imports format_xml/
	python3.12 -m mypy --ignore-missing-imports tests/
	python3.12 -m pylint ./format_xml/**
	python3.12 -m pylint ./tests/**

.PHONY: test
test:             ## Run 'general' tests and generate coverage report.
	python3.12 -m pytest -v --cov-config .coveragerc --cov=format_xml -l --tb=short --maxfail=1 tests/ -vm general
	python3.12 -m coverage xml
	python3.12 -m coverage html

.PHONY: test-verbose
test-verbose:     ## Run 'general' tests with verbose flag and generate coverage report.
	python3.12 -m pytest -vv --cov-config .coveragerc --cov=format_xml -l --tb=short --maxfail=1 tests/ -vm general
	python3.12 -m coverage xml
	python3.12 -m coverage html

.PHONY: test
test-justme:      ## Run individual tests by changing pytest.mark to 'justme' for spot-checking, with verbose flag.
	python3.12 -m pytest -vv --cov-config .coveragerc --cov=format_xml -l --tb=short --maxfail=1 tests/ -vm justme


.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr python3.12 -m pytest -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: clean
clean:            ## Clean unused files.
	@rm -rf .cache || true
	@rm -rf .pytest_cache || true
	@rm -rf .mypy_cache || true
	@rm -rf build || true
	@rm -rf dist || true
	@rm -rf *.egg-info || true
	@rm -rf htmlcov || true
	@rm -rf .tox/ || true
	@rm -rf docs-public/_build || true
	@rm -rf temp/ || true
	@find ./ -name '*.pyc' -exec rm -f {} \; || true
	@find ./ -name '__pycache__' -exec rm -rf {} \; || true
	@find ./ -name 'Thumbs.db' -exec rm -f {} \; || true
	@find ./ -name '*~' -exec rm -f {} \; || true
