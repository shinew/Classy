import urllib
import re
from HTMLParser import HTMLParser
from courseClasses import Course, Lecture, Tutorial, Reserve


class CustomHTMLParser(HTMLParser):
    """this class reads a HTML stream, then parses out the "data" fields"""

    def __init__(self, webData):
        HTMLParser.__init__(self)
        self.webData = webData

    def customInit(self, webData):
        """internalizes the webData attribute from the WebParser"""
        self.webData = webData

    def handle_data(self, data):
        """takes out the data"""
        self.webData.append(data.strip())


class WebParser:
    """"A WebParser is created for each and every course,
    to parse the corresponding web page"""

    requestURL = "http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"

    def __init__(self, courseString, session="1139"):
        self.webData = []
        self.index = -1
        self.thisCourse = None
        self.courseString = courseString
        # I chose to allow the Course class to parse the input string
        # for modularity
        self.thisCourse = Course(session, courseString)

    def run(self):
        """this is the method that the main class can call
        if successful, returns the Course class
        if not, returns an error message"""

        if self.getWebData():
            return "WebPageError"
        elif self.parseWebData():
            return "CourseNotFound"
        else:
            self.processCourseInfo()
            self.postProcess(self.thisCourse)
            return self.thisCourse

    def getWebData(self):
        """submits a POST query, initializes HTMLParser"""

        try:
            params = urllib.urlencode({"sess" : self.thisCourse.session,
                "subject" : self.thisCourse.subject})
            page = urllib.urlopen(self.requestURL, params)
            parser = CustomHTMLParser(self.webData)

            # we use .replace() because HTMLParser ignores "&nbsp",
            # which would screwn up our table
            parser.feed(page.read().replace("&nbsp", " "))
        except:
            return "WebPageError"

    def parseWebData(self):
        """We try to find the beginning of the desired table"""

        # now, we find the start index and pass that on along
        # with the webData
        for i in xrange(len(self.webData)):
            if self.webData[i] == self.thisCourse.subject \
                    and self.webData[i+2] == self.thisCourse.catalogNumber:
                        self.index = i
                        break
        if self.index == -1: # website not found
            return "CourseNotFound"


    def processCourseInfo(self):
        """now, we do the heavy-duty processing of the data table"""

        # sets basic attrs of thisCourse
        self.thisCourse.units = self.webData[self.index+4]
        self.thisCourse.title = self.webData[self.index+6]
        while self.webData[self.index] != "Instructor":
            self.index += 1

        # processing row-by-row
        while self.endOfRow(self.webData[self.index]) == False:
            if self.webData[self.index] != "":
                self.processSlot()
            self.index += 1

    def processSlot(self):
        """we check to see if this is the BEGINNING of a valid row"""

        if self.webData[self.index+1][:3].upper() == "LEC":
            # processing a lecture row
            lec = Lecture()
            self.processClass(lec, self.index, self.webData)
            self.thisCourse.lectures.append(lec)
        elif self.webData[self.index+1][:3].upper() == "TUT":
            # processing a tutorial row
            tut = Tutorial()
            self.processClass(tut, self.index, self.webData)
            self.thisCourse.tutorials.append(tut)
        elif self.webData[self.index][:7].upper() == "RESERVE":
            # processing a reserve row
            res = Reserve()
            self.processReserve(res, self.index, self.webData)
            self.thisCourse.lectures[-1].reserves.append(res)
        # note: we leave out the TST (exam?) times for now

    def processReserve(self, res, index, webData):
        """processing reservations for certain types of students"""

        # warning: we merge the next 4 cells together,
        # because the text is split between them
        reserveText = "".join(webData[index:index+3])

        # we leave out the first match, because it is the word "reserve"
        res.names = map(lambda x: x.strip(),
                re.findall(r"[\w\d\s\-\/]+", reserveText)[1:])

        # we remove the "only" suffix (which is annoyingly pointless)
        if "only" in res.names[-1]:
            res.names[-1] = res.names[:-5]

        # in case we took the enrollment numbers after it, we remove
        # number-suffixes (e.g. "1A students1200")
        while res.names[-1][-1].isdigit():
            res.names[-1] = res.names[-1][:-1]

        # now, we merge the match list
        while not webData[index].isdigit():
            index += 1

        # retriving enrollment numbers
        res.enrlCap = int(webData[index])
        res.enrlTotal = int(webData[index+1])

    def processClass(self, lec, index, webData):
        """we process a typical lecture or tutorial row"""

        attr1 = ["classNumber", "compSec", "campusLocation"]
        for i in xrange(len(attr1)):
            setattr(lec, attr1[i], webData[index+i].strip())
        index += 6

        attr2 = ["enrlCap", "enrlTotal", "waitCap", "waitTotal"]
        for i in xrange(len(attr2)):
            setattr(lec, attr2[i], int(webData[index+i]))
        index += 4

        # parsing the "Times Days/Date" field
        match = re.search(r"([:\d]+)-([:\d]+)(\w+)", webData[index])
        attr3 = ["startTime", "endTime", "days"]
        for i in xrange(len(attr3)):
            setattr(lec, attr3[i], match.group(i+1).strip())
        index += 1

        lec.building, lec.room = webData[index].split()
        lec.instructor = webData[index+1].strip()

    def endOfRow(self, data):
        """returns true if the current data-cell is the last cell
        of this course; else - false"""

        # the last cell is of the form: ##/##-##/##
        if re.search(r"\d+/\d+-\d+/\d+", data):
            return True
        else:
            return False

    def postProcess(self, course):
        """this function will convert the class times to minutes-past-
        the-previous-midnight, and converts the days
        to numbers"""

        for slot in course.lectures + course.tutorials:
            # first, we convert time to 24hr time
            # earliest start time for a class is 8:30am
            # night classes start at/before 7:00pm
            if 1 <= int(slot.startTime.split(":")[0]) <= 7:
                slot.startTime, slot.endTime = map(lambda x: "{}:{}".format\
                        (str(int(x.split(":")[0])+12), x[-2:]), [slot.startTime, slot.endTime])

            # now, we write to slot.sTime, slot.eTime (minutes-past-midnight...)
            slot.sTime, slot.eTime = map(lambda x: int(x[:2])*60+int(x[-2:]),
                    [slot.startTime, slot.endTime])

            # finally, we write to slot.ndays, where ndays is a string of numbers, 0->4

            if "M" in slot.days:
                slot.ndays += "0"

            i = slot.days.find("T")
            if i != -1  and (i == len(slot.days) - 1 or slot.days[i+1] != 'h'):
                # basically, if not Th (for Thursday)
                slot.ndays += "1"

            # now, for the rest of the days...
            for i in [("W", "2"), ("Th", "3"), ("F", "4")]:
                if i[0] in slot.days:
                    slot.ndays += i[1]
