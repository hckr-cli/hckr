.DEFAULT_GOAL := install # default command to run with just `make`
.PHONY: build publish package coverage test lint

env-default :
	hatch shell default

env-clean :
	hatch env prune

env-show :
	hatch env show

# install cli in local for testing, change code an it will be automatically reflected in UI
install:
	pip install -e .

package: clean
	hatch build

publish: package
	twine upload dist/*

clean :
	rm -rf dist \
	rm -rf docs/build \
	rm -rf *.egg-info \
	rm -f .coverage.*

test:
	hatch test

test-all:
	hatch test -a -p -r

coverage: clean
	hatch test --cover

lint:
	hatch run style:lint
#	hatch fmt --check

checks:
	hatch run types:check

lint-fix:
	hatch run style:fix
#	hatch fmt -f

