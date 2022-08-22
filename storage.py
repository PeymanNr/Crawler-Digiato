from abc import ABC, abstractmethod
import json


class StroageAbstract(ABC):
    @abstractmethod
    def store(self, data):
        pass

    @abstractmethod
    def load(self):
        pass


class MongoStorage(StroageAbstract):
    pass


class FileStorage(StroageAbstract):

    def store(self, data, filename, *args):
        with open(f'DataFolder/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
            print(f'DataFolder/{filename}.json')

    def load(self):
        with open('DataFolder/data.json', 'r') as f:
            links = json.loads(f.read())
        return links
