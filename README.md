# prometheus-node-exporter
Reactive subordinate charm providing prometheus-node-exporter.


# Usage
This charm relates to the prometheus charm on the `scrape` interface, and provides a metrics endpoint for prometheus to scrape on port 9100 by default.

A simple workflow to describe the usage of this charm is as follows:
```bash
juju deploy prometheus

juju deploy ubuntu

juju deploy prometheus-node-exporter

juju add-relation prometheus-node-exporter ubuntu

juju add-relation prometheus-node-exporter:scrape prometheus:scrape
```

# Configuration

Charm allows setting host and port to on which prometheus node exporter will listen. Host can be set also to "public" or "private" for charm to set according to unit.

Collectors which are disabled by default can be separately enabled in config (e.g. ntp, systemd, or nfs).

### Copyright
* James Beedy (c) 2017 <jamesbeedy@gmail.com>
* Tilman Baumann (c) 2019 <tilman.baumann@canonical.com>

### License
* AGPLv3 - see LICENSE
