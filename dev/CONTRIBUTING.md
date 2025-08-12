# hckr - Contributor's Guide

This Project is created and managed by [Ashish Patel](http://pateash.in/)

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

## Code changes
* After implementing code changes, you can run
```bash
make install
```
to install and link your hckr cli to existing code changes.

## Publishing to Pypi
* for publishing and creating tags refer
[Publishing Guide](PUBLISHING.md)

## Creating and maintaining Docs
* for Docs refer [Documentation Guide](DOCS.md)