.DEFAULT_GOAL := install
.PHONY: install install-dev

install:
	@pip install .
install-dev:
	@pip install '.[dev]'
