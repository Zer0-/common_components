import unittest
from os.path import join, exists
from bricks import Settings
from bricks import Bricks
from bricks.static_manager import StaticManager
from bricks.static_builder import establish_static_assets
from test_components.testcomponents import (
    testscss,
    testlib
)

class TestCompiledAssetCollection(unittest.TestCase):
    def setUp(self):
        self.pbricks = Bricks()
        for component in (
            Settings,
            StaticManager,
            testscss,
            testlib
        ):
            self.pbricks.add(component)

    def testAssetCopy(self):
        from os.path import exists
        out_dir = self.pbricks.components['json_settings']['static_buildout_dir']
        establish_static_assets(self.pbricks)
        self.assertTrue(exists(join(out_dir, 'scss', 'style.scss')))
        self.assertTrue(exists(join(out_dir, 'scss', 'scss_common', 'var.scss')))

    def testAssetUrl(self):
        scss = self.pbricks.components[testscss]
        self.assertEqual(scss.url, 'http://localhost:8888/scss/style.css')
    
if __name__ == '__main__':
    unittest.main()
