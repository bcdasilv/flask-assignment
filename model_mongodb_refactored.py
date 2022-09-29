import pymongo
from bson import ObjectId

class Model(dict):
    """
    A simple model that wraps mongodb document
    """
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self):
        if self.validate_fields():
            if not self._id:
                self.collection.insert_one(self)
                self._id = str(self._id)
                return True
        return False

    def reload(self):
        if self._id:
            result = self.collection.find_one({"_id": ObjectId(self._id)})
            if result :
                self.update(result)
                self._id = str(self._id)
                return True
        return False

    def remove(self):
        if self._id:
            resp = self.collection.delete_one({"_id": ObjectId(self._id)})
            return resp.deleted_count

class User(Model):
    db_client = pymongo.MongoClient('localhost', 27017)
    collection = db_client["users"]["users_list"]

    # def __init__(self, host, port, db_name, collection_name):
    #     self.db_client = pymongo.MongoClient(host, port)
    #     self.collection = self.db_client[db_name][collection_name]

    def find_all(self):
        users = list(self.collection.find())
        return self.convert_id_format(users)

    def find_by_name(self, name):
        users = list(self.collection.find({"name": name}))
        return self.convert_id_format(users)

    def find_by_name_job(self, name, job):
        users = list(self.collection.find({"name": name, "job": job}))
        return self.convert_id_format(users)

    def update_fields(self, fields):
        if self.reload() :
            update_result = self.collection.update_one(
                    { "_id": ObjectId(self._id) }, {'$set':fields } )
            if update_result.modified_count == 1 :
                self.update(fields)
                self._id = str(self._id)
                return 1
            return 0

    def convert_id_format(self, list_fromDB):
        for element in list_fromDB:
            element["_id"] = str(element["_id"])
        return list_fromDB

    def validate_fields(self):
        return self.name