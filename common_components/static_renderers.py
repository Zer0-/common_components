from os.path import join, splitext, basename
from bricks.staticfiles import StaticCss, StaticJs, StaticFile

class _BuiltStatic(StaticFile):
    has_build_stage = True

    def __init__(self, *args):
        StaticFile.__init__(self, *args)
        self.url = self.url.rsplit('.', 1)[0] + self.extension

class Sass(_BuiltStatic):
    relpath = 'scss'
    extension = '.css'
    target_type = 'css'

class Coffee(_BuiltStatic):
    relpath = 'coffee'
    extension = '.js'
    target_type = 'js'

class StaticLib(StaticFile):
    """A static asset or a directory with static assets that's needed
    to build other static assets but is not directly used by the page."""
    has_build_stage = True

    def __call__(self):
        return ''

class SassLib(StaticLib):
    relpath = 'scss'
