install:
  poetry install

plugins:
  poetry self add poetry-git-version-plugin

pre_commit:
  poetry run pre-commit install

setup: install plugins pre_commit

dev:
	mkdir -p .dagster && \
		cp dagster.yaml .dagster/dagster.yaml && \
		DAGSTER_HOME="$(pwd)/.dagster" poetry run dagster dev
