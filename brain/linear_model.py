from internal import NotEnoughDataException, grades, grade
from stats import covariance, simple_lr, multivariate_lr
from operator import add

def import_data(data):
    """Import from the db.gradebraindb.data mongo collection"""
    x = data.find()
    grades = []
    gradeset = []
    for x in data.find():
        person = []
        student = {}
        if 'semesters' in x['academics']:
            for y in x["academics"]["semesters"]:
                if type(y) == dict:
                    if "classes" in y:
                        for course in y["classes"]:
                            if(course["transcript"]):
                                if not (course["transcript"][0]["grade"] in ["P", "NP", "I"]):
                                    temp = { "class" : course["course_code"]}
                                    temp.update(*course["transcript"])
                                    person.append(temp)
                                    student[course["course_code"]] = course["transcript"][0]["grade"]
                    else:
                        raise "Invalid JSON!"
                else:
                    raise "Invalid JSON!"
        if len(person) > 0:
            grades.append(person)
            gradeset.append(student)
    return grades, gradeset

def student_had_class(student, classStr):
    """ Check if student took a class """
    for c in student:
        if c["class"] == classStr:
            return True
    return False

def get_student_grade(student, classStr):
    """ Find letter grade that a student got in a class """
    return filter(lambda c: c["class"] == classStr, student)[0]["grade"]

def histogram(dataset, class1, class2):
    """ Given data and two classes, return a dict of dicts that returns how many people that got a certain grade in one class got a grade in the second class """
    studentsThatTookClass = filter(lambda student: class1 in student and class2 in student, dataset)
    hist = {}
    for g in grades:
        hist[g] = dict.fromkeys(grades, 0)
    for student in studentsThatTookClass:
        hist[student[class1]][student[class2]] += 1
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

def get_multivar_lr(data, class1):
    """ Takes a class string and returns the linear regression coefficients
    for that class based on performance in ALL classes.

    throws an expception for invalid data
    data -- mongo GRADE data, NOT anything else
    class 1 -- string
    """
    gradeData = data[1]
    courses = list(set(map(lambda x: x["class"], reduce(add, data[0]))))
    courses.insert(0, "bias")
    all_class_grades = []
    class1_grades = []
    for student in gradeData:
        student_grades = [0] * len(courses)
        if class1 in student:
            for course in student.keys():
                student_grades[courses.index(course)] = grade(student[course])
            class1_grades.append(grade(student[class1]))
            all_class_grades.append(student_grades)
    if len(all_class_grades) != 0 and len(class1_grades) != 0:
        coeffs = multivariate_lr(all_class_grades, class1_grades)
        return dict(zip(courses, coeffs))
    else:
        raise "We don't have enough data to make a conclusion!"