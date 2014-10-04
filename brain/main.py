from pymongo import MongoClient
client = MongoClient('localhost', 27017)
data = client.gradebrain_development.data
for x in data.find():
    print(x)
