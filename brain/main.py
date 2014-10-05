from pymongo import MongoClient
from linear_model import *
from internal import *
from operator import add
import os

client = MongoClient('ds043350.mongolab.com', 43350)
client.gradebraindb.authenticate(
	os.environ["MONGO_USERNAME"],
	os.environ["MONGO_PASSWORD"],)
data = client.gradebraindb.data
models = client.gradebraindb.linear_models

"""
Write model to the db.gradebraindb.data mongo collection
class1, class2 are the course code strings, class1 < class2
linear_model is (b,a) for f = bx + a
"""

dataset = import_data(data)
classes = list(set(map(lambda x: x["class"], reduce(add, dataset))))

for class1 in classes:
    for class2 in classes:
        if class1 != class2:
            try:
                lm = get_lr_classes(dataset, class1, class2)
                hist = histogram(dataset, "COMPSCI 61A", "COMPSCI 61B")
                model = {"class1": class1, "class2": class2,
                    "model": {"t0": lm[1], "t1": lm[0]}, "histogram": hist}
            except NotEnoughDataException:
                hist = histogram(dataset, "COMPSCI 61A", "COMPSCI 61B")
                model = {"class1": class1, "class2": class2, "histogram": hist}
            models.remove({"class1": class1, "class2": class2})
            models.insert(model)