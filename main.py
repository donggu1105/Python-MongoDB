import pymongo
from pprint import pprint

username = "donggu"
password = "2245"
host = "3.35.255.138"
connection = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}")


books = connection.books

it_book = books.it_book

data = list()

for index in range(100):
    data.append({"author":"joey" , "publisher": "fun"})



books = it_book.find()

for book in books:
    print(book)

it_book.update_many({}, {"$set" : {"donggu" : "zzang"}})



