CHARM_NAME = prometheus-node-exporter
CHARM_SERIES = xenial
CHARM_OUTPUT = output

VIRT_ENV = $(PWD)/.ve
REQUIREMENTS_TXT = requirements.txt
export PATH := $(VIRT_ENV)/bin:$(PATH)


.PHONY: help
help: ## Print help about available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: $(VIRT_ENV) ## Install build dependencies and build the charm
	$(MAKE) charm-build

.PHONY: deps
deps:  ## Install the dependencies
	./dev/ubuntu-deps

.PHONY: charm-build
charm-build:  ## Build the charm
	rm -rf $(CHARM_OUTPUT)
	INTERFACE_PATH=interfaces charm build -s $(CHARM_SERIES) -o $(CHARM_OUTPUT)

$(CHARM_OUTPUT)/$(CHARM_SERIES)/$(CHARM_NAME):
	$(MAKE) charm-build

$(VIRT_ENV): deps
	python3 -m venv $(VIRT_ENV)
	pip install -r $(REQUIREMENTS_TXT)

.PHONY: test
test: CHARM_DIR=$(CHARM_OUTPUT)/$(CHARM_SERIES)/$(CHARM_NAME)
test:
	touch $(CHARM_DIR)/lib/charms/layer/__init__.py
	ln -sf $(PWD)/$(CHARM_DIR)/lib/charms/layer/ $(VIRT_ENV)/lib/python3.5/site-packages/charms/layer
	cd $(CHARM_DIR) && $(VIRT_ENV)/bin/python3 -m unittest discover unit_tests


.DEFAULT_GOAL := help
