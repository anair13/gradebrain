from internal import NotEnoughDataException, grades, grade
from stats import covariance, simple_lr

def import_data(data):
    """Import from the db.gradebraindb.data mongo collection"""
    x = data.find()
    grades = []
    for x in data.find():
        person = []
        if 'semesters' in x['academics']:
            for y in x["academics"]["semesters"]:
                if type(y) == dict:
                    if "classes" in y:
                        for course in y["classes"]:
                            if(course["transcript"]):
                                temp = { "class" : course["course_code"]}
                                temp.update(*course["transcript"])
                                person.append(temp)
                            
                    else:
                        raise "Invalid JSON!"
                else:
                    raise "Invalid JSON!"
        if len(person) > 0:
            grades.append(person)
    return grades

def write_model_to_mongo(data, class1, class2, linear_model):
    """Write model to the db.gradebraindb.data mongo collection
    class1, class2 are the course code strings, class1 < class2
    linear_model is (b,a) for f = bx + a
    """
    model = {"class1": class1, "class2": class2,
        "model": {"t0": linear_model[1], "t1": linear_model[0]}}
    data.insert(model)
    
def student_had_class(student, classStr):
    """ Check if student took a class """
    for c in student:
        if c["class"] == classStr:
            return True
    return False

def get_student_grade(student, classStr):
    """ Find letter grade that a student got in a class """
    return filter(lambda c: c["class"] == classStr, student)[0]["grade"]

def histogram(data, class1, class2):
    """ Given data and two classes, return a dict of dicts that returns how many people that got a certain grade in one class got a grade in the second class """
    studentsThatTookClass = filter(lambda student: student_had_class(student, class1) and student_had_class(student, class2), data)
    hist = dict.fromkeys(grades, dict.fromkeys(grades, 0))
    for student in studentsThatTookClass:
        hist[get_student_grade(student, class1)][get_student_grade(student, class2)] += 1
    return hist

def get_lr_samples(data, class1, class2):
    """ Takes two class strings and return samples that can be fed into regressions

    data -- mongo data from import_data()
    class1 -- String
    class2 -- String
    Returns [(class1grade, class2grade)]
    """

    validStudents = filter(lambda student: student_had_class(student, class1) and student_had_class(student, class2), data)
    grades = map(lambda student: (grade(get_student_grade(student, class1)), grade(get_student_grade(student, class2))), validStudents)

    return grades

def get_lr_classes(data, class1, class2):
    """ Takes two class strings and return the linear regression coefficients

    Throws a NotEnoughDataException if not enough data exists.

    data -- mongo data from import_data()
    class1 -- String
    class2 -- String
    Returns (b, a)
    """

    return simple_lr(get_lr_samples(data, class1, class2))
