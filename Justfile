test *args:
    uv run pytest {{args}}

guiding-test:
    uv run pytest guiding_test.py

update:
    uv sync --upgrade
