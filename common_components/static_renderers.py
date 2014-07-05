from os.path import join, splitext, basename
from bricks.staticfiles import StaticCss, StaticJs, StaticFile

class _BuiltStatic:
    has_build_stage = True

    def get_url(self):
        return self.static_url + join(
            self.relpath,
            splitext(basename(self.asset_path))[0] + self.extension
        )

class Sass(_BuiltStatic, StaticCss):
    relpath = 'scss'
    extension = '.css'

class Coffee(_BuiltStatic, StaticJs):
    relpath = 'coffee'
    extension = '.js'

class StaticLib(StaticFile):
    """A static asset or a directory with static assets that's needed
    to build other static assets but is not directly used by the page."""
    has_build_stage = True

    def __call__(self):
        return ''

class SassLib(StaticLib):
    relpath = 'scss'
