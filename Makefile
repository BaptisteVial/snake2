all:

lint:
	poetry run mypy
	poetry run ruff check

test:
	poetry run pytest

cov:
	poetry run coverage run -m pytest
	poetry run coverage report -m

clean:
	$(RM) -rf *.lock .venv */__pycache__

.PHONY: all clean lint test cov
