from common_components.static_renderers import Sass, Coffee, SassLib

asset_prefix = 'common_components:test/test_components/static/'

testscss = Sass("testscss", asset=asset_prefix + 'scss/style.scss')
testlib = SassLib('common_static', asset=asset_prefix + 'scss/scss_common')
