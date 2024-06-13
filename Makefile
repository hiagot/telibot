PYTHON := $(shell poetry env info -p)/Scripts/python

.PHONY: all
all: help

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run $(PYTHON) telibot/__main__.py

.PHONY: help
help:
	@echo "Makefile targets:"
	@echo "  install  - Install dependencies using Poetry"
	@echo "  run      - Run the application"
	@echo "  help     - Show this help message"
