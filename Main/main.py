import time
from webParser import WebParser
from matcher import Matcher
from profParser import RateMyProfParser

programStartTime = time.time()
sessionString = "fall 2013"
userCourses = ["math 135", "math 137", "cs 145", "afm 101", "econ 101"]

courses = []
for courseName in userCourses:
    tmp = WebParser(courseName, sessionString).run()
    courses.append(tmp)

# rateMyProfs
for i, course in enumerate(courses):
    print "Course {}/{}".format(str(i+1), len(courses))

    for j, slot in enumerate(course.lectures):
        print "Lecture {}/{}".format(str(j+1), len(course.lectures))
        ret = RateMyProfParser(slot.instructor).getInfo()
        if ret:
            slot.numRatings, slot.quality, slot.easiness = ret

    for j, slot in enumerate(course.tutorials):
        print "Tutorial {}/{}".format(str(j+1), len(course.tutorials))
        ret = RateMyProfParser(slot.instructor).getInfo()
        if ret:
            slot.numRatings, slot.quality, slot.easiness = ret

# now, we sort by ease, then quality, then number of ratings
for course in courses:
    course.lectures.sort(key=lambda x: (x.easiness, x.quality,
                                        x.numRatings), reverse=True)

# then we generate non-time-conflicting schedules
match = Matcher(courses)
generator = match.matching()

print "Time elapsed: {:.3f}".format(time.time() - programStartTime)

for schedule in generator:
    for slot in schedule:
        print slot
    print
    inp = raw_input("enter q to quit; enter n to continue: ")
    if inp.lower() == 'q':
        break
