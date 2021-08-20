from app.database import mongo_db
from bson.objectid import ObjectId

from app.operations.models import Extract, ExtractBase


class ExtractService:

    def __init__(self):
        self.db = mongo_db.extract

    def _get_item_by_id(self, id):
        return self.db.find_one({"_id": ObjectId(id)})

    def _update(self, id, data):
        query = {'_id': ObjectId(id)}
        values = {"$set": data}
        self.db.update_one(query, values)

    def get(self, id):
        return self._get_item_by_id(id)

    def get_all(self):
        extracts = []
        for extract in self.db.find():
            extracts.append(Extract(**extract))
        return extracts

    def create(self, extract: ExtractBase):
        self.db.insert_one(extract.dict(by_alias=True))
        return extract

    def delete(self, id):
        self.db.delete_one({"_id": ObjectId(id)})

    def update(self, id, data: ExtractBase):
        input_data = data.dict()
        new_data = {}
        for key, value in input_data.items():
            if input_data[key] != 'string':
                new_data[key] = value
        self._update(id, new_data)
        item = self._get_item_by_id(id)
        return item

