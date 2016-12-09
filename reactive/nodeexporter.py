from charms.reactive import (
    helpers,
    hook,
    when,
    when_not,
    set_state,
    remove_state,
    toggle_state,
)

@when('prometheus-client.available')
def prometheus_client(prometheus):
    prometheus.configure(port=9100)
