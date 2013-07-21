import pdb # for debugging purposes
import urllib
import re
from HTMLParser import HTMLParser
from courseClasses import Course, Lecture, Tutorial, Reserve


class CustomHTMLParser(HTMLParser):
    # this class reads the HTML page
    webData = []

    def customInit(self, data):
        # TODO: merge this under super()
        self.webData = data

    def handle_data(self, data):
        self.webData.append(data.strip())


class WebParser:
    """"This class is created for each and every course"""
    courseString = "" # "afm 101"
    requestURL = "http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"
    webData = []
    index = -1
    thisCourse = None

    def __init__(self, courseString, session="1139"):
        self.courseString = courseString
        self.thisCourse = Course(session, courseString)
        self.getWebData()

    def run(self):
        self.getWebData()
        self.parseWebData()
        if self.index == -1:
            return "website not found" # error 1 found
        else:
            return 0 # successfully completed

    def getWebData(self):
        # submitting POST form, initializing HTMLParser
        params = urllib.urlencode({"sess" : self.thisCourse.session, "subject" : self.thisCourse.subject})
        page = urllib.urlopen(self.requestURL, params)
        parser = CustomHTMLParser()
        parser.customInit(self.webData)
        parser.feed(page.read())

    def parseWebData(self):
        # now, we find the start index and pass that on along
        # with the webData
        self.findStartIndex()
        if self.index == -1: # website not found
            return
        self.processCourseInfo()

    def findStartIndex(self):
        # find the start index of the course, given webData is completed
        for i in xrange(len(self.webData)):
            if self.webData[i] == self.thisCourse.subject \
                    and self.webData[i+2] == self.thisCourse.catalogNumber:
                        self.index = i
                        break

    def processCourseInfo(self):
        # sets basic attrs of thisCourse
        self.thisCourse.units = self.webData[self.index+4]
        self.thisCourse.title = self.webData[self.index+6]
        while self.webData[self.index] != "Instructor":
            self.index += 1

        # to get to the first row of information
       # while not self.webData[self.index].isdigit():
        #    self.index += 1

        # processing row-by-row
        while self.isEnd(self.webData[self.index]) == False:
            if self.webData[self.index] != "":
                self.processSlot()
            self.index += 1

    def processSlot(self):
        if self.webData[self.index+1][:3].upper() == 'LEC':
            # processing a lecture row
            lec = Lecture()
            self.processClass(lec, self.index, self.webData)
            self.thisCourse.lectures.append(lec)
        elif self.webData[self.index+1][:3].upper() == 'TUT':
            # processing a tutorial row
            tut = Tutorial()
            self.processClass(tut, self.index, self.webData)
            self.thisCourse.tutorials.append(tut)
        elif self.webData[self.index][:7].upper() == 'RESERVE':
            # processing a reserve row
            res = Reserve()
            self.processReserve(res, self.index, self.webData)
            self.thisCourse.lectures[-1].reserves.append(res)
        # note: we leave out the TST (exam?) times for now

    def processReserve(self, res, index, webData):
        # warning: we merge the next 4 cells together, because the text is split between them
        reserveText = "".join(webData[index:index+3])

        # we leave out the first match, because it is the word "reserve"
        res.names = map(lambda x: x.strip(), re.findall(r'[\w\d\s\-\/]+', reserveText)[1:])

        # we remove the "only" suffix
        if "only" in res.names[-1]:
            res.names[-1] = res.names[:-5]

        # now, we merge the match list
        while not webData[index].isdigit():
            index += 1
        res.enrlCap = int(webData[index])
        res.enrlTotal = int(webData[index+1])
        pdb.set_trace()

    def processClass(self, lec, index, webData):
        # note that lec can be a tutorial as well
        # heavy-duty processing of the data array
        attr1 = ["classNumber", "compSec", "campusLocation"]
        for i in xrange(len(attr1)):
            setattr(lec, attr1[i], webData[index+i])
        index += 5

        attr2 = ["enrlCap", "enrlTotal", "waitCap", "waitTotal"]
        for i in xrange(len(attr2)):
            setattr(lec, attr2[i], int(webData[index+i]))
        index += 4

        # parsing the "Times Days/Date" field
        match = re.search(r'([:\d]+)-([:\d]+)(\w+)', webData[index])
        attr3 = ["startTime", "endTime", "days"]
        for i in xrange(len(attr3)):
            setattr(lec, attr3[i], match.group(i+1))
        index += 1

        lec.building, lec.room = webData[index].split()
        lec.instructor = webData[index+1]

    def isEnd(self, data):
        # returns true if the current data-cell is the last cell
        # of this course; else - false
        # the last cell is of the form: ##/##-##/##
        if re.search(r"\d+/\d+-\d+/\d+", data):
            return True
        else:
            return False
