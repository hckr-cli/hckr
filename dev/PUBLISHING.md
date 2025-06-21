# hckr — Publishing Guide

* Once we publish a release, Publish workflow [publish.yml](.github%2Fworkflows%2Fpublish.yml)
  automatically publishes a version to [PyPi](https://pypi.org/p/hckr)
  workflow will automatically create next tag using dynamic version defined in [__about
  __.py](src%2Fhckr%2F__about__.py)

## Pre-commits

* we use pre-commits to make sure we only push if lint and other checks are passed.
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

