import urllib
import re
from HTMLParser import HTMLParser
from CourseClasses import Course, Lecture, Tutorial


class customHTMLParser(HTMLParser):
    webData = []

    def customInit(self, data):
        # TODO: merge this under super()
        self.webData = data

    def handle_data(self, data):
        self.webData.append(data.strip())


class WebParser:
    """"This class is created for each and every course"""
    courseString = "" # "afm 101"
    session = "" # "1139"
    requestURL = "http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"
    webData = []
    index = -1
    thisCourse = None

    def __init__(self, courseString, session="1139"):
        self.courseString = courseString
        self.session = session
        self.thisCourse = Course(courseString)

    def getWebData(self):
        # submitting POST form, initializing HTMLParser
        params = urllib.urlencode({"sess" : self.session, "subject" : tmp.subject})
        page = urllib.urlopen(self.requestURL, params)
        parser = customHTMLParser()
        parser.customInit(self.webData)
        parser.feed(page.read())
        self.parseWebData()

    def parseWebData(self):
        # now, we find the start index and pass that on along
        # with the webData
        self.findStartIndex()
        self.processCourseInfo()

    def findStartIndex(self):
        #TODO: unit test invalid web pages ("course/session not found")
        # find the start index of the course, given webData is completed
        for i in xrange(len(self.webData)):
            if webData[i] == self.thisCourse.subject and webData[i+1] == self.thisCourse.catalogNumber:
                self.index = i
                break

    def processCourseInfo(self):
        # sets basic attrs of thisCourse
        self.thisCourse.units = self.webData[self.index+2]
        self.thisCourse.title = self.webData[self.index+3]
        while self.webData[self.index] != "Instructor":
            self.index += 1
        self.index += 1

    def isEnd(self, data):
        # returns true if the current data-cell is the last cell
        # of this course; else - false
        # the last cell is of the form: ##/##-##/##
        if re.search(r"\d+/\d+-\d+/\d+", data):
            return True
        else:
            return False
