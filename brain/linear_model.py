from main import data # Temporary

class NotEnoughDataException(Exception):
    pass

def import_data(data):
    """Import from the db.gradebraindb.data mongo collection"""
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

def simple_lr(samples):
    """Returns linear regression coefficients (b, a) where f = bx + a
    samples :: [(Float, Float)]

    Throws a NotEnoughDataException if not enough data exists.
    """
    xs, ys = list(map(lambda a: a[0], samples)), list(map(lambda a: a[1], samples))
    avgx = sum(xs) / len(xs)
    avgy = sum(ys) / len(ys)
    bnum = sum([(xs[i] - avgx) * (ys[i] - avgy) for i in range(len(samples))])
    bdenom = sum([(xs[i] - avgx) ** 2 for i in range(len(samples))])
    if bnum == 0 or bdenum == 0:
        raise NotEnoughDataException("Not enough data! Regression model has a coefficient of 0 or infinity")
    b = bnum / bdenom
    a = avgy - b * avgx
    return (b, a)

def write_model_to_mongo(data, class1, class2, linear_model):
    """Write model to the db.gradebraindb.data mongo collection
    class1, class2 are the course code strings, class1 < class2
    linear_model is (b,a) for f = bx + a
    """
    model = {"class1": class1, "class2": class2,
        "model": {"t0": linear_model[1], "t1": linear_model[0]}}
    data.insert(model)

def get_lr_classes(data, class1, class2):
    """ Takes two class strings, where class1 < class2, and return the linear regression coefficients

    Throws a NotEnoughDataException if not enough data exists.

    data -- mongo data from import_data()
    class1 -- String
    class2 -- String
    Returns (b, a)
    """
    # Convert grade letter to number
    def grade(letter):
        return {
                    "A+" : 100
                  , "A" : 95
                  , "A-" : 90
                  , "B+" : 88
                  , "B" : 85
                  , "B-" : 80
               }[letter]

    # Find all students that took both classes
    def student_had_class(student, classStr):
        """ Check if student took a class """
        for c in student:
            if c["class"] == classStr:
                return True
        return False

    # Find grade that a student got in a class
    def get_student_grade(student, classStr):
        return filter(lambda c: c["class"] == classStr, student)[0]["grade"]

    validStudents = filter(lambda student: student_had_class(student, class1) and student_had_class(student, class2), data)
    grades = map(lambda student: (grade(get_student_grade(student, class1)), grade(get_student_grade(student, class2))), validStudents)

    return simple_lr(grades)

d = import_data(data)
