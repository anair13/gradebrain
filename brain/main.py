
from pymongo import MongoClient
import os
def import_data():
	client = MongoClient('ds043350.mongolab.com', 43350)

	client.gradebraindb.authenticate(
		os.environ["MONGO_USERNAME"],
		os.environ["MONGO_PASSWORD"],
		)
	data = client.gradebraindb.data
	x = data.find()
	grades = []
	for x in data.find():
		it = iter(x)
		if 'semesters' in x['academics']:
			for y in x["academics"]["semesters"]:
				if type(y) == dict:
					if "classes" in y:
						person = []
						for course in y["classes"]:
							if(course["transcript"]):
								temp = { "class" : course["course_code"]}
								temp.update(*course["transcript"])
								person.append(temp)
							
					else:
						raise "Invalid JSON!"
				if len(person) > 0:
					grades.append(person)
	return grades
