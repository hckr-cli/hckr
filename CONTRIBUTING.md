# hckr - Contributor's Guide

This Project is created and managed by [Ashish Patel](http://pateash.in/)

## Table of Contents

- [Releasing Version/Tag](#releasing-versiontag)
- [Publishing to PyPi](#publishing-to-pypi)
- [Pre-commit Checks](#pre-commits)

Please Contribute to this project by forking [hckr](https://github.com/pateash/hckr/)

Please feel free to provide any suggestion for new utility in [Issues](https://github.com/pateash/hckr/issues)

## Publishing to Pypi
* Once we publish a release, Publish workflow [publish.yml](.github%2Fworkflows%2Fpublish.yml) automatically publishes a version to  [PyPi](https://pypi.org/p/hckr)
workflow will automatically create next tag using dynamic version defined in [__about__.py](src%2Fhckr%2F__about__.py)

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
