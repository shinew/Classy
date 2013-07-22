from webParser import WebParser
from matcher import Matcher

sessionString = "fall 2013"
userCourses = ["math 135", "math 137", "cs 145", "afm 101", "econ 101"]

courses = []
for courseName in userCourses:
    tmp = WebParser(courseName, sessionString).run()
    courses.append(tmp)

match = Matcher(courses)
generator = match.matching()

for schedule in generator:
    for slot in schedule:
        print slot
    print
    inp = raw_input("enter q to quit; enter n to continue: ")
    if inp.lower() == 'q':
        break
