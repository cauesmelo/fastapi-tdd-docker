# Test-Driven Development with FastAPI and Docker

[![Continuous Integration and Delivery](https://github.com/cauesmelo/fastapi-tdd-docker/actions/workflows/main.yml/badge.svg)](https://github.com/cauesmelo/fastapi-tdd-docker/actions/workflows/main.yml)

##  Commands

Run Flake8
> `flake8 .`

Run Black
> `black .`

Run isort
> `isort .`

Run all tests
> `pytest`

Code coverage report
> `pytest --cov="."`

Code coverage report HTML
> `pytest --cov="." --cov-report html`

Parallel unit test
> `pytest -k "unit" -n auto`