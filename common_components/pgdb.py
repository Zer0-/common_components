"""PyramidBricks component that provides a connection to a Postgresql Database"""

from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
import psycopg2 as postgres

class PostgresDatabaseComponenet:
    provides = ['postgres']
    requires_configured = ['json_settings']

    def __init__(self, settings):
        self.dbsettings = settings['database']
        self.pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=settings['database']['conn_pool_size'],
            database=self.dbsettings['name'],
            user=self.dbsettings['username'],
            password=self.dbsettings['password'],
            host=self.dbsettings['host'],
            port=self.dbsettings.get('port')
        )

    @property
    @contextmanager
    def cursor(self):
        connection = self.pool.getconn()
        try:
            with connection.cursor() as cursor:
                yield cursor
            connection.commit()
        finally:
            self.pool.putconn(connection)
