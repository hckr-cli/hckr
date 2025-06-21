# hckr - Contributor's Guide

This Project is created and managed by [Ashish Patel](http://pateash.in/)

## Table of Contents

- [Releasing Version/Tag](#releasing-versiontag)
- [Publishing to PyPi](#publishing-to-pypi)
- [Pre-commit Checks](#pre-commits)

Please Contribute to this project by forking [hckr](https://github.com/hckr-cli/hckr/)

Please feel free to provide any suggestion for new utility
in [Issues](https://github.com/hckr-cli/hckr/issues)

## Python

* Use python3.8+ in development
    * if not available use following commands
      ```bash
      pyenv install 3.8
      pyenv virtualenv 3.8 py38
      pyenv activate py38 
      pip install hatch # then install hatch to start using it
      ```
* use the following command to step into **hatch** defined python venv

  ``make sync-dev``

## Publishing to Pypi

* Once we publish a release, Publish workflow [publish.yml](.github%2Fworkflows%2Fpublish.yml)
  automatically publishes a version to [PyPi](https://pypi.org/p/hckr)
  workflow will automatically create next tag using dynamic version defined in [__about
  __.py](src%2Fhckr%2F__about__.py)

## Pre-commits

* we use pre-commits to make sure we only pushes if lint and other checks are passed.
* Install `pre-commit` from pypi and install in Git to enable this.

```bash 
pip install pre-commit
pre-commit install
```

## Dev versions cleanup

* we can easily clean up all the dev version using this command.

```shell
 make pypi-clean
```

## Homebrew formulae

Please find a contributing guide for `Homebrew formulae` here [HOMEBREW.md](HOMEBREW.md)

## Senty integration

[Sentry console](https://hckr-cli.sentry.io/projects/hckr/?project=4507910060572672)
