import os
from hashlib import md5
import logging
log = logging.getLogger(__name__)

class FileStore:
    def __init__(self, root_path, max_dirsize=1000, files_upperbound=10**5):
        """root path is where FileStore will start its directory tree."""
        self.root_path = root_path
        import math
        self.wordlen = math.floor(math.log(max_dirsize, 16))
        self.pathlen = math.ceil(math.log(files_upperbound, max_dirsize) - 1)
        self.identlen = self.wordlen * self.pathlen

    def tree_resolve(self, identifier):
        return '/'.join([identifier[i:i+self.wordlen] for i in range(
                            0, self.identlen, self.wordlen)])

    def create_identifier(self, bin_data):
        return md5(bin_data).hexdigest()[:self.identlen]

    def save(self, filename, bin_data, identifier=None):
        """there better not be any '/' chars in the filename you hear!"""
        if identifier is None:
            identifier = self.create_identifier(filename.encode('utf-8'))
        path = self.get_filepath(filename, identifier)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as out:
            out.write(bin_data)
        log.info("wrote file {}".format(path))
        return identifier

    def get_filepath(self, filename, identifier):
        return os.path.join(self.root_path, self.get(filename, identifier))

    def get(self, filename, identifier):
        return os.path.join(self.tree_resolve(identifier), filename)

    def delete(self, filename, identifier):
        os.remove(self.get_filepath(filename, identifier))
