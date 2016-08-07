import unittest
from os.path import join, exists
import tempfile
from bricks import Settings
from bricks import Bricks
from bricks.static_manager import StaticManager
from bricks.static_builder import establish_static_assets
from common_components.test.test_components.testcomponents import (
    testscss,
    testlib
)

class MockSettings(dict):
    provides = ['json_settings']

    def __init__(self, location=None):
        dict.__init__(self)
        self['static_buildout_dir'] = tempfile.tempdir
        self['served_static_url'] = 'http://localhost:8888/'

class TestCompiledAssetCollection(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        tempfile.gettempdir()

    def setUp(self):
        bricks = Bricks()
        self.settings = bricks.add(MockSettings)
        bricks.add(StaticManager)
        self.testscss = bricks.add(testscss)
        bricks.add(testlib)
        self.bricks = bricks

    def testAssetCopy(self):
        from os.path import exists
        out_dir = self.settings['static_buildout_dir']
        establish_static_assets(self.bricks)
        self.assertTrue(exists(join(out_dir, 'test_components', 'static', 'style.scss')))
        self.assertTrue(exists(join(out_dir, 'static', 'scss_common', 'var.scss')))

    def testAssetUrl(self):
        self.assertEqual(self.testscss.url, 'http://localhost:8888/test_components/static/style.css')
    
if __name__ == '__main__':
    unittest.main()
