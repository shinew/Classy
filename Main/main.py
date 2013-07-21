from webParser import WebParser

mysession = "fall 2013"
mycourses = ["math 135", "math 137", "cs 145", "afm 101", "econ 101"]
courses = []
for i in mycourses:
    tmp = WebParser(i)
    tmp2 = tmp.run()
    courses.append(tmp2)
