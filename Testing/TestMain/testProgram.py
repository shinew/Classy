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
import sys


# we want to make sure all courses are do-able
def queryUniversity(userCourses, courses, user, sessionString):
    for courseName in userCourses:
        newCourse = WebParser().run(courseName, sessionString)
        courses.append(newCourse)
        if type(newCourse) is str:
            print "An error has occured with {0}: " \
                  "{1}. {0} will be ignored.".format(courseName, newCourse)
            with open("errors.txt", "a") as f:
                f.write("{}\t{}\n".format(courseName, newCourse))
            courses.pop()

def main():
    # variables
    userCourses = [sys.argv[1].replace("-", " ")]
    courses = []
    user = User()
    sessionString = "fall 2013"

    # program starts here
    queryUniversity(userCourses, courses, user, sessionString)

if __name__ == "__main__":
    main()
