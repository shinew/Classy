from webParser import WebParser
from matcher import Matcher
from profParser import RateMyProfParser

sessionString = "fall 2013"
userCourses = ["math 135", "math 137", "cs 145", "afm 101", "econ 101"]

courses = []
for courseName in userCourses:
    tmp = WebParser(courseName, sessionString).run()
    courses.append(tmp)

# rateMyProfs
for i, course in enumerate(courses):
    print "Doing course", i
    for slot in course.lectures:
        ret = RateMyProfParser(slot.instructor).getInfo()
        if ret:
            slot.numRatings, slot.quality, slot.easiness = ret
    for slot in course.tutorials:
        ret = RateMyProfParser(slot.instructor).getInfo()
        if ret:
            slot.numRatings, slot.quality, slot.easiness = ret

# now, we sort by rating
for course in courses:
    course.lectures.sort(key = lambda x: )


# then we generate non-time-conflicting schedules
match = Matcher(courses)
generator = match.matching()

for schedule in generator:
    for slot in schedule:
        print slot
    print
    inp = raw_input("enter q to quit; enter n to continue: ")
    if inp.lower() == 'q':
        break
