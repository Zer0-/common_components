from pyramid.path import AssetResolver
from pyramid_bricks.staticfiles import StaticCss, StaticJs, StaticFile
from pyramid_bricks.component import CustomComponent

class Sass(StaticCss):
    has_build_stage = True
    relpath = 'scss'

class Coffee(StaticJs):
    has_build_stage = True
    relpath = 'coffee'

class StaticLib(StaticFile):
    """A static asset or a directory with static assets that's needed
    to build other static assets but is not directly used by the page"""
    custom_attributes = ('asset',)
    has_build_stage = True

    def __call__(self):
        return ''

class SassLib(StaticLib):
    relpath = 'scss'
