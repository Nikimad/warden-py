.PHONY: test test-one lint lint-fix format format-check typecheck check

test:
	python -m uv run pytest -v

# make test-one T=tests/test_parse.py::test_extract_image_url
test-one:
	python -m uv run pytest -v $(T)

lint:
	python -m uv run ruff check .

lint-fix:
	python -m uv run ruff check . --fix

format:
	python -m uv run ruff format .

format-check:
	python -m uv run ruff format . --check

typecheck:
	python -m uv run mypy

check: lint format-check typecheck test
