.PHONY: test
test:
	@tox

build:
	@charm build -rl DEBUG

push:
	@charm push `echo $(JUJU_REPOSITORY)`/builds/prometheus-node-exporter cs:~jamesbeedy/prometheus-node-exporter
