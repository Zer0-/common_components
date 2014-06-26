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
        self.bricks.add(Settings)
        self.pool = self.bricks.add(SqliteThreadPool)
        self.db = self.bricks.add(DatabaseComponent)

    def test_trivial(self):
        with self.db.cursor as cursor:
            pass
        self.assertEqual(len(self.pool.connections), 1)

    def testExec(self):
        with self.db.cursor as cursor:
            cursor.execute("SELECT 1, 'two';")
            result = cursor.fetchone()
        self.assertEqual(result, (1, 'two'))
        self.assertEqual(len(self.pool.connections), 1)

    def testPool(self):
        import threading
        connections = set()
        threads = set()
        def target():
            c = self.pool.getconn()
            connections.add(c)
            self.pool.putconn(c)

        for i in range(3):
            t = threading.Thread(target=target)
            t.start()
            threads.add(t)
        for thread in threads:
            thread.join()
        self.assertEqual(len(connections), 3)
        self.assertEqual(len(self.pool.connections), 3)
    
if __name__ == '__main__':
    unittest.main()
