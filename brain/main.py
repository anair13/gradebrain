from pymongo import MongoClient
import os

client = MongoClient('ds043350.mongolab.com', 43350)
client.gradebraindb.authenticate(
	os.environ["MONGO_USERNAME"],
	os.environ["MONGO_PASSWORD"],)
data = client.gradebraindb.data

