test *args:
    uv run pytest {{args}}

update:
    uv sync --upgrade
