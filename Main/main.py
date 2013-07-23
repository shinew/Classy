"""
Copyright 2013 Shine Wang

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from webParser import WebParser
from matcher import Matcher
from profParser import RateMyProfParser
from user import User


def getUserInfo(userCourses):
    print "Hello! I am Classy, and I'll optimize your course selection."
    print "The current optimizations are:"
    print "1.\tno time conflicts."
    print "2.\tsorting by ratemyprofessor.com ratings.\n"
    print "Please follow prompts VERY CLOSELY!"

    #sessionString = raw_input("Which session you are in? (e.g. 'fall 2013' "
    #                          "without quotes): ").strip().lower()
    sessionString = "fall 2013"  # we really don't need this atm

    print "\nPlease add courses in decreasing importance."
    print "Format: 'cs 145' (without quotes)"

    cour = ""
    while cour.strip() != "0":
        cour = raw_input("Enter '0' to stop adding: ").strip().upper()
        userCourses.append(cour)
    userCourses.pop()  # the last '0'
    return sessionString


def queryUniversity(userCourses, courses, user, sessionString):
    print "Currently querying adm.uwaterloo.ca..."
    for courseName in userCourses:
        newCourse = WebParser().run(courseName, sessionString)
        courses.append(newCourse)
        if type(newCourse) is str:
            print "An error has occured with {0}: " \
                  "{1}. {0} will be ignored.".format(courseName, newCourse)
            courses.pop()
    print "Done!\n"

    print "Which reservation categories apply to you?"

    askedNames = set()
    for course in courses:
        for lec in course.lectures:
            if lec.thisUserCanAdd or len(lec.reserves) == 0:
                continue
            for res in lec.reserves:
                if res.enrlCap - res.enrlTotal <= 0:
                    # this reservation has no spots left anyway,
                    # so don't ask
                    continue
                for name in res.names:
                    if name in askedNames:
                        # don't want to re-ask
                        continue

                    askedNames.add(name)
                    inp = raw_input("Enter 'y' if you fufill the "
                                    "reservation of \"{}\". If not, "
                                    "enter 'n': ".format(name))
                    if inp.lower() == 'y':
                        user.userTypes.add(name)

            lec.postProcess(user.userTypes)


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
    print "Done!\n"


def postProcessing(courses):
    """sort by ease, then quality, then number of ratings"""
    for course in courses:
        course.lectures.sort(key=lambda x: (x.easiness, x.quality,
                                            x.numRatings), reverse=True)
        course.tutorials.sort(key=lambda x: (x.easiness, x.quality,
                                             x.numRatings), reverse=True)


def scheduleGeneration(courses):
    """generates a schedule"""

    print "All calculations complete!"
    print "You will be given a chance to save your selected schedule " \
          "later."
    print "Format is: "
    attrs = ["Class#", "CompSec", "Place", "Start", "End", "Days",
             "Building Room", "Instructor"]
    print "{:8}\t".format("Course"),
    print "\t".join(attrs)

    generator = Matcher(courses).matching()
    schedule = ""
    for schedule in generator:
        for slot in schedule:
            print slot
        print
        inp = raw_input("enter 's' to save the last schedule to a file; "
                        "enter 'n' to see another possible schedule: ")
        if inp.lower() == 's':
            return schedule
    print "\nSorry! No more schedules left! :(\n"
    return schedule


def saveToFile(schedule):
    """saves to file"""

    print "Would you like to save the last schedule to a file?"

    ans = raw_input("Enter 'y' if you do; 'n' if you don't: ").lower()
    if ans != 'y':
        print "Okay. Have a nice day then!"

    else:
        outputFile = raw_input("\nPlease enter a file name: ")
        f = open(outputFile+".txt", "w")
        for slot in schedule:
            f.write(str(slot) + "\n")
        f.close()

        print "\nOkay! The file is saved at {}. Have a nice " \
              "day.".format(outputFile+".txt")

    raw_input("Enter anything to exit: ")


def main():
    # variables
    userCourses = []
    courses = []
    user = User()
    sessionString = ""

    # program starts here
    sessionString = getUserInfo(userCourses)
    queryUniversity(userCourses, courses, user, sessionString)
    queryRateMyProfessors(courses)
    postProcessing(courses)
    lastSchedule = scheduleGeneration(courses)
    saveToFile(lastSchedule)

if __name__ == "__main__":
    main()
