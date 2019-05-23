from charmhelpers.core.host import (
    service_restart,
    service_running,
    service_start,
)


NODE_EXPORTER_BIN = "/usr/bin/node_exporter"
NODE_EXPORTER_SERVICE = "/etc/systemd/system/node-exporter.service"


def start_restart(service):
    if service_running(service):
        service_restart(service)
    else:
        service_start(service)
