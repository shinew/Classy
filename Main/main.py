from webParser import WebParser
from matcher2 import Matcher

mysession = "    fall 2013     "
mycourses = ["math 135", "math 137", "cs 145", "afm 101", "econ 101"]
courses = []
for i in mycourses:
    tmp = WebParser(i, mysession).run()
    courses.append(tmp)

mat = Matcher(courses)
a = mat.matching()
