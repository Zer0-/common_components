from .filestore import FileStore

class FileStoreComponent(FileStore):
    provides = ['file_store']
    requires_configured = ['json_settings']

    def __init__(self, settings):
        FileStore.__init__(self, settings['user_content_directory'])
        self.media_url = settings['user_content_serve_root_url']

    def geturl(self, filename, identifier):
        return self.media_url + self.get(filename, identifier)
