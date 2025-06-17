# Contributing
You are free to work on any bug fix or feature from the issues tab. If you intend to do so, please create a new issue if it doesn't yet exist, and assign yourself to the issue so that we know someone is actively working on it.

# Developing
Below is a small guide for getting your environment set up and running/testing the tool. We use [poetry](https://python-poetry.org/docs/) to manage
dependencies.

## Getting started and getting the latest dependencies
```bash
poetry install
```

## Running tests manually
We have a Travis CI setup that will run the test suite, perfrom python linting, and verify the code has full testing coverage for every commit you
push. It will perform these checks for every python version that we support, and your code will need to pass all these checks in order to get merged
in. You can also running these checks manually before you push your code out as well:
```bash
# Run the test suite manually using your system's default python version:
poetry run pytest --cov-report term --cov=ws_rebalancer

# Run the linter against the project's default python version
poetry run flake8

# Run the test suite against all the supported python versions
# and the linter in an isolated environment. You will need to
# have the supported python versions installed otherwise you
# will get a `InterpreterNotFoundError`
poetry run tox
```

## Running the tool manually
```
poetry run ws-rebalancer ...
```

## Creating a release
Once you have all the changes you desire for a release, do the following. Note that
we follow [semantic versioning](https://semver.org/) for our projects.

1. Create a new branch
2. Bump up the release numbers in `pyproject.toml`
3. Push + create PR. Once PR is ready, merge it into the main branch.
4. Create a new release using the Github release tools. This will create a new tag and
kick off a CI build. The ensuing CI build will notice that this is a tagged commit and
will package the project and push it to PyPI.
