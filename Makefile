###########################
# Hardware Abstraction Layer
# We use Docker to provide a source-controlled build enviroment.
###########################

# --------------- DECLARATIONS  ----------------------------------------------#

IMAGENAME=hardware-abstraction-layer
CONTAINERNAME=hardware-abstraction-layer

ENV_HASH=$(shell cat enviroment/Dockerfile enviroment/apt-list | shasum -a 1 | tr " " "\n" | head -n 1)

BUILD_THREADS := $(shell cat /proc/cpuinfo | grep processor | wc -l)

ifeq ($(OS),Windows_NT)
  # Windows is not supported!
else
  # Some commands are different in Linux and Mac
  UNAME_S := $(shell uname -s)

	# Credential of the user will be passed to the image and container
	USERNAME := $(shell whoami)
	USER_UID := $(shell id -u)
	USER_GID := $(shell id -g)
endif

# Passing arguments to documentation builder in specifications/Makefile
# i.e. `make specs command` in ./ --> `make command` in ./specifications/
# 
# For HTML documentation run `make specs html`, then
# open specs/_build/html/index.html in your favourite browser.
# 
# Ref https://stackoverflow.com/a/14061796
# Ref https://stackoverflow.com/a/9802777/3454146
FORSPECS=$(firstword $(MAKECMDGOALS))
ifeq ($(FORSPECS), $(filter $(FORSPECS), specs dev-specs))
  SPECS_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(SPECS_ARGS):;@:)
endif


DBUILD=docker build . \
	--file ./environment/Dockerfile \
	--tag ${IMAGENAME} \
	--build-arg USERNAME=${USERNAME} \
	--build-arg USER_UID=${USER_UID} \
	--build-arg USER_GID=${USER_GID}

DRUN=docker run \
	--interactive \
	--privileged \
	--rm \
	--volume ${PWD}:/workdir \
	--workdir /workdir \
	--name=${CONTAINERNAME} 

DEXEC=docker exec \
     --interactive \
     $(shell cat container)

PYCODESTYLE=pycodestyle -v \
	examples/ test/ >> pycodestyle.log || true

PYLINT=pylint \
	--rcfile=pylint.rc \
	lib/ test/ >> pylint.log

PYTEST=pytest \
	-v \
	-ra \
	--random-order \
	--log-level=INFO \
	--junitxml=testreport.xml \
	--cov-report xml \
	--cov-report term

MAKEPACKAGE=python3 setup.py sdist bdist_wheel

CHECKPACKAGE=python3 -m twine check dist/*

TESTUPLOADPACKAGE=python3 -m twine upload \
	--repository testpypi \
	-u $(user) \
	-p $(pass) \
	dist/*

UPLOADPACKAGE=python3 -m twine upload \
     -u $(user) \
     -p $(pass) \
     dist/*

# --------------- DOCKER STUFF -----------------------------------------------#
.PHONY: build
build: ./environment/Dockerfile ## Build the image
	${DBUILD}

.PHONY: build-nc
build-nc: ./environment/Dockerfile ## Build the image from scratch
	${DBUILD} --no-cache

container: 
	make build
	${DRUN} \
	--detach \
	--cidfile=container \
	${IMAGENAME} \
	/bin/bash  

.PHONY: shell
shell: container
	docker exec -it $(shell cat container) /bin/bash

# --------------- QA ---------------------------------------------------------#
.PHONY: pylint
pylint: container ## Run code quality checker
	${DEXEC} ${PYLINT}

.PHONY: pycodestyle
pycodestyle: container ## Run PEP8 checker
	${DEXEC} ${PYCODESTYLE}

# --------------- SPECIFICATIONS ---------------------------------------------#
.PHONY: specs
specs: container ## Generate specs
	${DEXEC} make -C specs $(SPECS_ARGS)

# --------------- PYPI SERVER ------------------------------------------------#
.PHONY: build-package
build-package: container ## Make the package
	${DEXEC} ${MAKEPACKAGE}
	${DEXEC} ${CHECKPACKAGE}

.PHONY: test-upload-package
test-upload-package: build-package ## Make and upload the package to test.pypi.org
	${DEXEC} ${TESTUPLOADPACKAGE}

.PHONY: upload-package
upload-package: build-package ## Make and upload the package to pypi.org
	${DEXEC} ${UPLOADPACKAGE}

# --------------- TESTING ----------------------------------------------------#
.PHONY: test
test: test-nose ## Run all the tests

.PHONY: test-nose
test-nose: container ## Run the test suite via nose
	${DEXEC} ${PYTEST}

.PHONY: test-unit
test-unit: container ## Run the test suite via unittest
	${DEXEC} python -m unittest -v

.PHONY: check-os
check-os: ## Which OS is used?
ifeq ($(OS),Windows_NT)
	@echo MAKEFILE: Windows is detected (not supported!)
else ifeq ($(UNAME_S),Linux)
	@echo MAKEFILE: Linux is detected
else ifeq ($(UNAME_S),Darwin)
	@echo MAKEFILE: Mac is detected
else
	@echo MAKEFILE: What is this beast?
endif

# --------------- CLEANING ---------------------------------------------------#

PHONY: clean
clean: clean-logs clean-cache clean-data clean-container ## Clean everything

.PHONY: clean-cache
clean-cache: ## Clean python cache
ifeq ($(UNAME_S),Linux)
	find . -name "__pycache__" -type d -print0 | xargs -r0 -- rm -r
	find . -name "*.pyc" -type f -print0 | xargs -r0 -- rm -r
else
	find . -name "*.pyc" -type f -exec rm -rf {} \;
	find . -name "__pycache__" -type d -exec rm -rf {} \;
endif

.PHONY: clean-container
clean-container: ## Stop and remove the container
	docker ps -q --filter "name=${CONTAINERNAME}" | grep -q . && \
	docker stop ${CONTAINERNAME}
	rm -f container

.PHONY: clean-cover
clean-cover: ## Clean the test suite results
	rm -f .coverage coverage.xml nosetests.xml trace.vcd

.PHONY: clean-data
clean-data: ## Clean any data
	rm -f *.vcd *.png *.txt

.PHONY: clean-logs
clean-logs: ## Clean logs
	rm -f pylint.log pycodestyle.log

# Commands from this section are meant to be used ONLY inside of
# the development container via VSCode

.PHONY: dev-test
dev-test: dev-test-nose ## See non-dev version

.PHONY: dev-test-nose
dev-test-nose: ## See non-dev version
	${PYTEST}

.PHONY: dev-test-unit
dev-test-unit: ## See non-dev version
	python -m unittest discover

.PHONY: dev-pylint
dev-pylint: ## See non-dev version
	${PYLINT}

.PHONY: dev-pycodestyle
dev-pycodestyle: ## See non-dev version
	${PYCODESTYLE}

.PHONY: dev-clean

dev-clean: clean-cache clean-cover clean-data clean-logs ## See non-dev version
