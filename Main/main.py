import time
from webParser import WebParser
from matcher import Matcher
from profParser import RateMyProfParser


# default values left for debugging
sessionString = "fall 2013"
# userCourses = ["math 135", "math 137", "cs 145", "afm 101", "econ 101"]
userCourses = []
courses = []
generator = None
myTime = time.time()

def programTime():
    print "This program took {:.2f}s to complete.".format(time.time()
                                                          - myTime)

def getUserInfo(userCourses):
    print "HI there! I am Classy, and I'll optimize your course selection."
    sessionString = raw_input("Please tell me which session are in " \
            "(e.g. 'fall 2013' without quotes): ")
    cour = ""
    while cour.strip() != "0":
        cour = raw_input("Please add a course (e.g. 'math 145' " \
                "without quotes).\nEnter '0' (without quotes) to" \
                " stop adding: ")
        userCourses.append(cour)
    userCourses.pop()  # the last '0'

def queryUniversity(userCourses, courses):
    print "Currently querying adm.uwaterloo.ca..."
    for courseName in userCourses:
        tmp = WebParser(courseName, sessionString).run()
        courses.append(tmp)

def queryRateMyProfessors(courses):
    print "Currently querying ratemyprofessors.com..."

    for i, course in enumerate(courses):
        print "Process: Course {}/{}".format(str(i+1), len(courses))

        for j, slot in enumerate(course.lectures):
            #print "Lecture {}/{}".format(str(j+1), len(course.lectures))
            ret = RateMyProfParser(slot.instructor).getInfo()
            if ret:
                slot.numRatings, slot.quality, slot.easiness = ret

        for j, slot in enumerate(course.tutorials):
            #print "Tutorial {}/{}".format(str(j+1), len(course.tutorials))
            ret = RateMyProfParser(slot.instructor).getInfo()
            if ret:
                slot.numRatings, slot.quality, slot.easiness = ret

def postProcessing(courses):
    # sort by ease, then quality, then number of ratings
    for course in courses:
        course.lectures.sort(key=lambda x: (x.easiness, x.quality,
                                            x.numRatings), reverse=True)

    # then we generate non-time-conflicting schedules

def scheduleGeneration(generator):
    print "All calculations complete!"
    print "You will be given a chance to save your selected schedule" \
          " later."

    generator = Matcher(courses).matching()

    for schedule in generator:
        if schedule is None:
            break
        for slot in schedule:
            print slot
        print
        inp = raw_input("enter 'q' to quit and save your file;" \
                        " enter 'n' to see the next schedule: ")
        if inp.lower() == 'q':
            break
    outputFile = raw_input("Where would you like to save this schedule?" \
          " Please enter a file name: ")
    f = open(outputFile, "w")
    for slot in schedule:
        f.write(repr(slot) + "\n")
    f.close()

getUserInfo(userCourses)
queryUniversity(userCourses, courses)
queryRateMyProfessors(courses)
postProcessing(courses)
# programTime()
scheduleGeneration(generator)
