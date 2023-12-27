install:
  poetry install

plugins:
  poetry self add poetry-git-version-plugin

pre_commit:
  poetry run pre-commit install

setup: install plugins pre_commit

dev:
  poetry run invoke dagster-dev
