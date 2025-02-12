from pymongo import MongoClient

#CREATE  a local mongdb connection
client=MongoClient("mongodb://localhost:27017/")

# CREATE A DATABASE
db=client["users"]

# CREATE A COLLECTION
users=db.get_collection("usersdata")
tasks=db.get_collection('tasks')
category_collection=db.get_collection("category")

