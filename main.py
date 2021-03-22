import pymongo
from pprint import pprint

username = "donggu"
password = "2245"
host = "3.35.255.138"
connection = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}")


db = connection.test_db


result = db.zip.aggregate([
    {'$group' : {

        '_id' : 'null',
        'count' : {'$sum' : 1}

    }}
])



for col in result:
    print(col)