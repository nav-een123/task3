# from pymongo import MongoClient


# #CREATE  a local mongdb connection

# client=MongoClient("mongodb://localhost:27017/")

# # CREATE A DATABASE
# db=client["users"]

# # CREATE A COLLECTION
# collection=db.get_collection("usersdata")


# def insert_data():
#     # Sample users Data
#     user= [
#     {"name": "Alice", "age": 28, "department": "HR", "salary": 50000},
#     {"name": "Bob", "age": 34, "department": "IT", "salary": 70000},
#     {"name": "Charlie", "age": 25, "department": "Finance", "salary": 55000},
#     {"name": "David", "age": 40, "department": "IT", "salary": 90000},
#     {"name": "Emma", "age": 30, "department": "Marketing", "salary": 60000},
#     {"name": "Frank", "age": 29, "department": "HR", "salary": 52000},
#     {"name": "Grace", "age": 27, "department": "Finance", "salary": 58000},
#     {"name": "Henry", "age": 35, "department": "IT", "salary": 80000},
#     {"name": "Ivy", "age": 32, "department": "Marketing", "salary": 62000},
#     {"name": "Jack", "age": 31, "department": "Sales", "salary": 65000},
#     {"name": "Kate", "age": 26, "department": "HR", "salary": 48000},
#     {"name": "Leo", "age": 38, "department": "Finance", "salary": 75000},
#     {"name": "Mia", "age": 29, "department": "Sales", "salary": 63000},
#     {"name": "Noah", "age": 33, "department": "IT", "salary": 77000},
#     {"name": "Olivia", "age": 28, "department": "Marketing", "salary": 59000},
#     {"name": "Paul", "age": 36, "department": "Finance", "salary": 72000},
#     {"name": "Quinn", "age": 30, "department": "HR", "salary": 51000},
#     {"name": "Ryan", "age": 27, "department": "IT", "salary": 68000},
#     {"name": "Sophia", "age": 34, "department": "Sales", "salary": 67000},
#     {"name": "Tom", "age": 31, "department": "Marketing", "salary": 61000}
# ]

 # Insert multiple users records
#     collection.insert_many(user)

# insert_data()

from pymongo import MongoClient


 #CREATE  a local mongdb connection

client=MongoClient("mongodb://localhost:27017/")

 # CREATE A DATABASE
db=client["users"]

# CREATE A COLLECTION
users=db.get_collection("usersdata")
tasks=db.get_collection('tasks')



