import re

class UrlMapper:
    provides = ['url_mapper']
    def __init__(self, mappings):
        self.mappings = mappings

    def resolve(self, url):
        for regex, map in self.mappings.items():
            if re.match(regex, url) is not None:
                return map(url)
        return url
