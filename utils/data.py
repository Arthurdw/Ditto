# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from os import getenv

from cassandra.cluster import Cluster

from .db_statements import stmt


class ScyllaDB:
    keyspace = 'ditto'
    hosts = [host.strip().lower() for host in getenv("DB_HOST").split(',')]

    def __init__(self):
        self.cluster = Cluster(self.hosts)
        self.session = self.cluster.connect()

    def __setup_db(self):
        self.session.execute(stmt.keyspace_init.format(keyspace=self.keyspace))
        self.session.set_keyspace(self.keyspace)
