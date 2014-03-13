import __main__
import os

def read_settings(filepath=None):
    from json import loads
    if filepath is None:
        if hasattr(__main__, '__file__'):
            here = os.path.dirname(__main__.__file__)
        else:
            here = os.path.dirname(__file__)
        filepath = os.path.join(here, 'settings.local.json')
        if not os.path.exists(filepath):
            filepath = os.path.join(here, 'settings.json')
        if not os.path.exists(filepath):
            raise IOError('settings.json file cannot be found!')
    with open(filepath, 'r') as jsonsettings:
        return loads(jsonsettings.read())

class Settings(dict):
    provides = ['json_settings']

    def __init__(self):
        dict.__init__(self)
        self.update(read_settings())
        self['project_dir'] = os.path.dirname(__file__)
