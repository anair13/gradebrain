from pymongo import MongoClient
from linear_model import *
from internal import *
from operator import add
from stats import *
import os

#local_client = MongoClient()
client = MongoClient('ds043350.mongolab.com', 43350)
client.gradebraindb.authenticate(
	os.environ["MONGO_USERNAME"],
	os.environ["MONGO_PASSWORD"],)
data = client.gradebraindb.data
models = client.gradebraindb.linear_models
courses = client.gradebraindb.courses
#models = local_client.gradebrain_development.linear_models

"""
Write model to the db.gradebraindb.data mongo collection
class1, class2 are the course code strings, class1 < class2
linear_model is (b,a) for f = bx + a
"""
dataset, gradeset = import_data(data)
classes = list(set(reduce(add,map(lambda x: x.keys(), gradeset))))
print(classes)

for class1 in classes:
    for class2 in classes:
        print(class1, class2)
        if class1 != class2:
            hist = histogram(gradeset, class1, class2)
            try:
                lm = get_lr_classes(dataset, class1, class2)
                se = stdev(get_lr_samples(dataset, class1, class2))
                model = {"class1": class1, "class2": class2,
                    "model": {"t0": lm[1], "t1": lm[0], "se": se, "histogram": hist}}
            except NotEnoughDataException:
                model = {"class1": class1, "class2": class2, "model": {"histogram": hist}}
            models.remove({"class1": class1, "class2": class2})
            models.insert(model)

# multivariate regression
for clazz in classes:
    print(clazz)
    courses.insert({"name": clazz, "dirty": False})

    try:
        coeffs = get_multivar_lr((dataset, gradeset), classes[:], clazz)
        model = {"class1": clazz, "class2": "x", "model": coeffs}
        models.remove({"class1": clazz, "class2": ""})
        models.remove({"class1": clazz, "class2": "x"})
        models.insert(model)
    except NotEnoughDataException:
        pass