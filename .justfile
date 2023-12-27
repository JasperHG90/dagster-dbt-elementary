requirements:
  pip install -r requirements.txt --upgrade pip && dbt deps

dev_requirements:
  pip install -r dev_requirements.txt --upgrade pip

pre_commit:
  pre-commit install

install: requirements dev_requirements pre_commit
