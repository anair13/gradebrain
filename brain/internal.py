class NotEnoughDataException(Exception):
    pass

grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]

# Convert grade letter to number
def grade(letter):
    return {
                "A+" : 100
              , "A" : 95
              , "A-" : 90
              , "B+" : 88
              , "B" : 85
              , "B-" : 80
              , "C+" : 78
              , "C" : 75
              , "C-" : 70
              , "D+" : 68
              , "D" : 65
              , "D-" : 60
              , "F" : 50
           }[letter]
