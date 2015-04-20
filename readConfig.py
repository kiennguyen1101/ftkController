import ConfigParser
import os.path

from collections import OrderedDict

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict, self).__setitem__(key, value)

config = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
config.read('config.ini')
path = config.get('DEFAULT', 'path')
FTK_IMAGER_PATH = False
for item in path:
    if os.path.exists(item):
        FTK_IMAGER_PATH = item        
        
print FTK_IMAGER_PATH