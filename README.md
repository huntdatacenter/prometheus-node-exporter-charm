# prometheus-node-exporter
Reactive subordinate charm providing prometheus-node-exporter.


# Usage
This charm relates to the prometheus charm on the `scrape` interface, and will provide a metrics endpoint for prometheus to scrape on port 9100 by default.

A simple workflow to describe the usage of this charm is as follows:
```bash
juju deploy prometheus

juju deploy ubuntu

juju deploy prometheus-node-exporter

juju add-relation prometheus-node-exporter ubuntu

juju add-relation prometheus-node-exporter:scrape prometheus:scrape
```

### Copyright
* James Beedy (c) 2017 <jamesbeedy@gmail.com> 
* Tilman Baumann (c) 2019 <tilman.baumann@canonical.com>
 
### License
* AGPLv3 - see LICENSE
