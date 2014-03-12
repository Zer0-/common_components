from pyramid_bricks.staticfiles import StaticFile

class Sass(StaticFile):
    requires_configured = ['url_mapper'] + StaticFile.requires_configured

    def __init__(self, url_mapper, *args):
        super(Sass, self).__init__(*args)
        self.asset = url_mapper.resolve(self.asset)

    def __call__(self):
        return '<link rel="stylesheet" href="{}" />'.format(self.asset)

class Coffee(Sass):
    def __call__(self):
        return '<script src="{}"></script>'.format(self.asset)
