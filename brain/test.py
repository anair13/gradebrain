from pymongo import MongoClient
from linear_model import *
from internal import *
from operator import add
from stats import *
import os

local_client = MongoClient()
client = MongoClient('ds043350.mongolab.com', 43350)
client.gradebraindb.authenticate(
    os.environ["MONGO_USERNAME"],
    os.environ["MONGO_PASSWORD"],)
data = client.gradebraindb.data
models = client.gradebraindb.linear_models
#models = local_client.gradebrain_development.linear_models

"""
Write model to the db.gradebraindb.data mongo collection
class1, class2 are the course code strings, class1 < class2
linear_model is (b,a) for f = bx + a
"""

dataset = import_data(data)
gradeset = import_grades(data)
print(gradeset)
classes = list(set(map(lambda x: x["class"], reduce(add, dataset))))
print(histogram(gradeset, "COMPSCI 61A", "COMPSCI 61B"))