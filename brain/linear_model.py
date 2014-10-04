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
    """
    xs, ys = list(map(lambda a: a[0], samples)), list(map(lambda a: a[1], samples))
    avgx = sum(xs) / len(xs)
    avgy = sum(ys) / len(ys)
    bnum = sum([(xs[i] - avgx) * (ys[i] - avgy) for i in range(len(samples))])
    bdenom = sum([(xs[i] - avgx) ** 2 for i in range(len(samples))])
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
