from charmhelpers.core.host import service as service_cmd
from charmhelpers.core.host import (
    service_restart,
    service_running,
    service_start
)

NODE_EXPORTER_BIN = "/usr/bin/prometheus-node-exporter"
NODE_EXPORTER_SERVICE = "/etc/systemd/system/prometheus-node-exporter.service"
NODE_EXPORTER_DEFAULT = "/etc/default/prometheus-node-exporter"


def start_restart(service):
    if service_running(service):
        service_restart(service)
    else:
        service_start(service)


def service_enable(service):
    service_cmd('enable', service)


def service_disable(service):
    service_cmd('disable', service)
