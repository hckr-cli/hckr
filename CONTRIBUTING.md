# hckr - Contributing Guide

This Project is created and managed by [Ashish Patel](http://pateash.in/)

## Table of Contents

- [Releasing Version/Tag](#Releasing Version/Tag)
- [License](#license)

Please Contribute to this project by forking [hckr](https://github.com/pateash/hckr/)

Please feel free to provide any suggestion for new utility in [Issues](https://github.com/pateash/hckr/issues)

## Releasing Version/Tag
* Tags workflow [tags.yml](.github%2Fworkflows%2Ftags.yml) automatically creates tag using dynamic version defined in [__about__.py](src%2Fhckr%2F__about__.py)

### Publishing to Pypi
* Once we publish a release, Publish workflow [publish.yml](.github%2Fworkflows%2Fpublish.yml) automatically publishes a version to  [PyPi](https://pypi.org/p/hckr)


### Pre-commits
* we use pre-commits to make sure we only pushes if lint and other checks are passed.
* Install `pre-commit` from pypi and install in Git to enable this.
```bash 
pip install pre-commit
pre-commit install
```

## Sponsors
> Built using Jetbrains Products
![Jetbrains](https://www.jetbrains.com/company/brand/img/jetbrains_logo.png)
