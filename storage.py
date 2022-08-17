from abc import ABC
import json


class StroageAbstract(ABC):

    def store(self, data):
        pass


class MongoStorage(StroageAbstract):
    pass


class FileStorage(StroageAbstract):

    def store(self, data, filename,  *args):
        with open(f'data/{filename}.json', 'w') as f:
            f.write(json.dumps(data))

