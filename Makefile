.DEFAULT_GOAL := install # default command to run with just `make`
.PHONY: build publish package coverage test lint docs

env-prune :
	hatch env prune

env-show :
	hatch env show

hatch-docs-deps-sync:
	hatch run docs:docs-deps

sync-default:
	hatch run default:deps

sync-dev:
	hatch run dev:deps

sync-docs:
	hatch run docs:deps

# Sync only happens when we change something in deps array
# to simulate we can add a dependency 'cowsay' to a env and sync
sync : sync-default sync-dev sync-docs hatch-docs-deps-sync fix

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
	rm -f .coverage.* \
	rm -f coverage.xml

test:
	hatch test -- -vvv

test-verbose:
	hatch test -- -vvv  --capture=no

test-all:
	hatch test -a -p -r

coverage: clean
	hatch test --cover -vvv -- --capture=no
	hatch run dev:cov-xml

lint:
	hatch run dev:lint
#	hatch fmt --check

check:
	hatch run dev:check

# this checks for any error in local github action files, https://nektosact.com/
# using dryrun with -n and -v for verbose
gha:
	act -g


# all checks
checks: lint check test

fix:
	hatch run dev:fix
#	hatch fmt -f

deps:
	hatch dep show table

pypi-clean:
	hatch run dev:pypi-clean

docs-build:
	cd docs/ && make clean && make html && cd ..

docs:
	hatch run docs:docs

# this if for local testing only
run:
	which hckr
	hckr
