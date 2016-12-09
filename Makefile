CHARM_NAME = prometheus-node-exporter
CHARM_SERIES = xenial
CHARM_OUTPUT = ../prometheus-node-exporter-charm-output


.PHONY: help
help: ## Print help about available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Install build dependencies and build the charm
	./dev/ubuntu-deps
	$(MAKE) charm-build

.PHONY: charm-build
charm-build:  ## Build the charm
	rm -rf $(CHARM_OUTPUT)
	INTERFACE_PATH=interfaces charm build -s $(CHARM_SERIES) -o $(CHARM_OUTPUT)

$(CHARM_OUTPUT)/$(CHARM_SERIES)/$(CHARM_NAME):
	$(MAKE) charm-build


.DEFAULT_GOAL := help
