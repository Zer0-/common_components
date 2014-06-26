import unittest
from common_components.db import SqliteThreadPool, DatabaseComponent
from pyramid_bricks import Bricks

settings = {
    'database': {
        'name': ':memory:'
    }
}

class Settings(dict):
    provides = ['json_settings']

    def __init__(self):
        dict.__init__(self)
        self.update(settings)

class TestSqliteComponent(unittest.TestCase):
    def setUp(self):
        self.bricks = Bricks()
        for component in (
            Settings,
            SqliteThreadPool
        ):
            self.bricks.add(component)
        self.db = self.bricks.add(DatabaseComponent)

    def test_trivial(self):
        with self.db.cursor as cursor:
            pass

    def testExec(self):
        with self.db.cursor as cursor:
            cursor.execute("SELECT 1, 'two';")
            result = cursor.fetchone()
        self.assertEqual(result, (1, 'two'))

    def testPool(self):
        import threading
        connections = set()
        pool = self.bricks.components[SqliteThreadPool]
        threads = set()
        def target():
            c = pool.getconn()
            connections.add(c)
            pool.putconn(c)

        for i in range(3):
            t = threading.Thread(target=target)
            t.start()
            threads.add(t)
        for thread in threads:
            thread.join()
        self.assertEqual(len(connections), 3)
        self.assertEqual(len(pool.connections), 3)
    
if __name__ == '__main__':
    unittest.main()
