# RSE bot

[![Test and build](https://github.com/ImperialCollegeLondon/poetry_template_2/actions/workflows/ci.yml/badge.svg)](https://github.com/ImperialCollegeLondon/poetry_template_2/actions/workflows/ci.yml)

A tool to analyse whether your code follows best practices.

:construction: This code is currently in pre-alpha stage. :construction:

Currently it only works with public repositories on GitHub.

To run, first install dependencies via poetry:

```sh
poetry install
```

Run it for a given repository like so:

```sh
python -m ic_rse_bot ImperialCollegeLondon/FINESSE
```

The tool will then generate a report highlighting issues with the given repository.
