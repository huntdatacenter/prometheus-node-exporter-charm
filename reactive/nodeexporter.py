from charms.reactive import when
from charmhelpers.core import hookenv


@when('prometheus-client.available')
def prometheus_client(prometheus):
    prometheus.configure(port=9100)

    principal_unit = get_principal_unit()
    for relation_id in hookenv.relation_ids('prometheus-client'):
        hookenv.relation_set(relation_id, {'principal-unit': principal_unit})


def get_principal_unit():
    '''Return the principal unit for this subordinate.'''
    relation_ids = hookenv.relation_ids('container')
    if not relation_ids:
        return

    relations = hookenv.relations_for_id(relation_ids[0])
    if relations:
        return relations[0]['__unit__']
