import os
from shutil import copyfile
from subprocess import call

from charms.reactive import (
    when,
    hook,
    when_not,
    set_state,
)
from charms.reactive.relations import endpoint_from_flag, endpoint_from_name
from charms.reactive.flags import clear_flag

from charmhelpers.core.hookenv import (
    config,
    resource_get,
    status_set,
    open_port,
    unit_private_ip,
    unit_public_ip,
    log,
)

from charmhelpers.core.templating import render
from charmhelpers.core.host import (
    mkdir,
    group_exists,
    add_group,
    user_exists,
    adduser,
    service_stop,
)
from charms.layer.prometheus_node_exporter import (
    start_restart,
    NODE_EXPORTER_BIN,
    NODE_EXPORTER_SERVICE,
    NODE_EXPORTER_DEFAULT,
)


@hook('config-changed')
def render_default_config():
    enabled_collectors = []
    for collector in [
        'ntp', 'nfs', 'supervisord', 'systemd', 'mountstats', 'interrupts',
        'bonding', 'megacli', 'tcpstat', 'runit',  'qdisc', 'ksmt', 'logind',
        'gmond', 'drbd', 'buddyinfo'
    ]:
        if config('{}-collector'.format(collector)):
            enabled_collectors.append(collector)

    ctxt = {
        'debug': config('debug'),
        'collectors': enabled_collectors,
    }
    render(
        'prometheus-node-exporter-default.tmpl',
        NODE_EXPORTER_DEFAULT,
        context=ctxt
    )
    start_restart('prometheus-node-exporter')


@when_not('prometheus.user.available')
def create_prometheus_user():
    if not group_exists('prometheus'):
        add_group('prometheus', system_group=True)
    if not user_exists('prometheus'):
        adduser(
            'prometheus',
            shell='/bin/false',
            system_user=True,
            primary_group='prometheus',
            home_dir='/var/lib/prometheus',
        )
    set_state('prometheus.user.available')


@when('prometheus.user.available')
@when_not('prometheus.dir.available')
def create_prometheus_directory():
    if not os.path.exists('/var/lib/prometheus'):
        mkdir('/var/lib/prometheus', owner='prometheus')
    if not os.path.exists('/var/lib/prometheus/node-exporter'):
        mkdir('/var/lib/prometheus/node-exporter', owner='prometheus')
    set_state('prometheus.dir.available')


@when_not('prometheus.node.exporter.bin.available')
def install_prometheus_exporter_resource():
    go_bin = resource_get('node-exporter')
    if os.path.exists(NODE_EXPORTER_BIN):
        os.remove(NODE_EXPORTER_BIN)
    copyfile(go_bin, NODE_EXPORTER_BIN)
    call('chmod +x {}'.format(NODE_EXPORTER_BIN).split())
    set_state('prometheus.node.exporter.bin.available')


@when('prometheus.node.exporter.bin.available',
      'prometheus.dir.available')
@when_not('prometheus.node.exporter.systemd.available')
def render_systemd_config():
    if os.path.exists(NODE_EXPORTER_SERVICE):
        os.remove(NODE_EXPORTER_SERVICE)
    if os.path.exists(NODE_EXPORTER_DEFAULT):
        os.remove(NODE_EXPORTER_DEFAULT)
    host = config('host')
    if host in ['public', 'private']:
        host = unit_private_ip() if (host == 'private') else unit_public_ip()
    ctxt = {
        'host': host,
        'port': config('port')
    }
    render_default_config()
    render(
        'prometheus-node-exporter.service.tmpl',
        NODE_EXPORTER_SERVICE,
        context=ctxt
    )
    set_state('prometheus.node.exporter.systemd.available')


@when('prometheus.node.exporter.bin.available',
      'prometheus.node.exporter.systemd.available',
      'prometheus.dir.available')
@when_not('prometheus.node.exporter.available')
def set_prometheus_node_exporter_available():
    start_restart('prometheus-node-exporter')
    open_port(config('port'))
    status_set("active", "Prometheus-Node-Exporter Running on port {}".format(
        config('port')
    ))
    set_state('prometheus.node.exporter.available')


@when('config.changed.port',
      'prometheus.node.exporter.available')
def port_changed():
    prometheus = endpoint_from_name('scrape')
    log("Port changed, telling relations. ({})".format(
        config('port')
    ))
    prometheus.configure(port=config('port'))


@when('prometheus.node.exporter.available',
      'endpoint.scrape.available')
@when_not('prometheus.node.exporter.configured_port')
def set_provides_data():
    prometheus = endpoint_from_flag('endpoint.scrape.available')
    log("Scrape Endpoint became available. Telling port. ({})".format(
        config('port')
    ))
    prometheus.configure(port=config('port'))
    set_state('prometheus.node.exporter.configured_port')


@when_not('endpoint.scrape.available')
@when('prometheus.node.exporter.configured_port')
def prometheus_left():
    log("Scrape Endpoint became unavailable")
    clear_flag('prometheus.node.exporter.configured_port')


@hook('stop')
def cleanup():
    status_set("maintenance", "cleaning up prometheus-node-exporter")
    service_stop('prometheus-node-exporter')
    for f in [NODE_EXPORTER_BIN, NODE_EXPORTER_SERVICE]:
        call('rm {}'.format(f).split())
    status_set("active", "cleanup complete")
