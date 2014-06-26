import threading
from contextlib import contextmanager

class SqliteThreadPool:
    provides = ['db_connection_pool']
    requires_configured = ['json_settings']

    def __init__(self, settings):
        import sqlite3
        from collections import defaultdict
        connstr = settings['database']['name']
        self.connections = defaultdict(lambda: sqlite3.connect(connstr))

    def getconn(self):
        thread_id = threading.current_thread().ident
        connection = self.connections[thread_id]
        del self.connections[thread_id]
        return connection

    def putconn(self, connection):
        thread_id = threading.current_thread().ident
        if thread_id in self.connections:
            raise ValueError("A connection was already returned by this thread.")
        self.connections[thread_id] = connection

class PostgresThreadPool:
    provides = ['db_connection_pool']
    requires_configured = ['json_settings']

    def __init__(self, settings):
        from psycopg2.pool import ThreadedConnectionPool
        dbsettings = settings['database']
        self.pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=settings['database']['conn_pool_size'],
            database=dbsettings['name'],
            user=dbsettings['username'],
            password=dbsettings['password'],
            host=dbsettings['host'],
            port=dbsettings.get('port')
        )

    def getconn(self):
        return self.pool.getconn()

    def putconn(self, connection):
        return self.pool.putconn(connection)

class DatabaseComponent:
    provides = ['sql_database']
    requires_configured = ['db_connection_pool']

    def __init__(self, pool):
        self.pool = pool

    @property
    @contextmanager
    def cursor(self):
        connection = self.pool.getconn()
        try:
            yield connection.cursor()
            #Note we're not closing cusrors. PG will close them at the end of the transaction
            #unless we're using WITH HOLD (we're not)
            connection.commit()
        except:
            connection.rollback()
            raise
        finally:
            self.pool.putconn(connection)
