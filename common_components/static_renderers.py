from os.path import join, splitext, basename
from bricks.staticfiles import StaticCss, StaticJs, StaticFile

class _BuiltStatic(StaticFile):
    has_build_stage = True

    def __init__(self, *args):
        StaticFile.__init__(self, *args)
        self.url = self.url.rsplit('.', 1)[0] + '.' + self.target_type

class Sass(_BuiltStatic):
    relpath = 'scss'
    target_type = 'css'

    def __call__(self):
        return '<link rel="stylesheet" href="{}" />'.format(self.url)

class Coffee(_BuiltStatic):
    relpath = 'coffee'
    target_type = 'js'

    def __call__(self):
        return '<script src="{}"></script>'.format(self.url)

class StaticLib(StaticFile):
    """A static asset or a directory with static assets that's needed
    to build other static assets but is not directly used by the page."""
    has_build_stage = True

    def __call__(self):
        return ''

class SassLib(StaticLib):
    relpath = 'scss'
