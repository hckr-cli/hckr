.DEFAULT_GOAL := install # default command to run with just `make`
.PHONY: build publish package coverage test lint

env-default :
	hatch shell default

env-clean :
	hatch env prune

env-show :
	hatch env show

# this will sync the dependencies automatically
sync :
	hatch run cowsay -t "Syncing Dependencies" && echo "Synced.\n============="

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
	hatch test -- -v

test-all:
	hatch test -a -p -r

coverage: clean
	hatch test --cover

lint:
	hatch run dev:lint
#	hatch fmt --check

checks: lint
	hatch run dev:check

lint-fix:
	hatch run dev:fix
#	hatch fmt -f

show-deps:
	hatch dep show table
