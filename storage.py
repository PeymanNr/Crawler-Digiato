from abc import ABC, abstractmethod
import json
from mongo import Mongodatabase


class StroageAbstract(ABC):
    @abstractmethod
    def store(self, data):
        pass

    @abstractmethod
    def load(self):
        pass


class MongoStorage(StroageAbstract):
    def __init__(self):
        self.mongo = Mongodatabase()

    def store(self, data, collection, *args):
        collection = getattr(self.mongo.database, collection)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)

    def load(self):
        return self.mongo.database.adv_links.find({'flag': False})

    def update_flag(self, data):
        self.mongo.database.adv_links.find_one_and_update(
            {'_id': data['_id']}, {'$set': {'flag': True}}
        )


class FileStorage(StroageAbstract):

    def store(self, data, filename, *args):
        with open(f'DataFolder/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
            print(f'DataFolder/{filename}.json')

    def load(self):
        with open('DataFolder/adv_links.json', 'r') as f:
            links = json.loads(f.read())
        return links
