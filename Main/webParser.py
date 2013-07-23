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


import urllib
import re
from HTMLParser import HTMLParser
from courseClasses import Course, Lecture, Tutorial, Reserve


class CustomHTMLParser(HTMLParser):
    """this class reads a HTML stream, then parses out the "data" fields"""

    def __init__(self, webData):
        HTMLParser.__init__(self)
        self.webData = webData

    def handle_data(self, data):
        """takes out the data"""
        self.webData.append(data.strip())


class WebParser:
    """"A WebParser is created for each and every course,
    to parse the corresponding web page"""

    requestURL = "http://www.adm.uwaterloo.ca/cgi-bin/" \
                 "cgiwrap/infocour/salook.pl"

    def __init__(self):
        self.webData = []
        self.index = -1
        self.session = None
        self.thisCourse = None

    def run(self, courseString, sessionString):
        """this is the method that the main class can call
        if successful, returns the Course class
        if not, returns an error message"""

        self.session = self.parseSession(sessionString)
        if self.session is None:
            return "SessionNameWrongError"

        courseString = map(lambda x: x.upper(), courseString.split())
        try:
            self.thisCourse = Course(self.session, courseString[0],
                                     courseString[1])
        except:
            return "CourseNameWrongError"

        if self.getWebData(self.thisCourse):
            return "WebPageError"
        elif self.parseWebData():
            return "CourseNotFoundError"
        else:
            self.processCourseInfo()
            self.postProcess(self.thisCourse)
            return self.thisCourse

    def parseSession(self, sessionString):
        try:
            ret = "1"
            ret += sessionString.split()[1][-2:]  # last 2 digits of year
            tempMap = (("fall", "9"), ("winter", "1"), ("spring", "5"))
            for season in tempMap:
                if season[0] in sessionString.lower():
                    ret += season[1]
                    return ret
        except:
            return None

    def getWebData(self, course):
        """submits a POST query, initializes HTMLParser"""

        try:
            params = urllib.urlencode({"sess": course.session,
                                       "subject": course.subject,
                                       "cournum": course.catalogNumber})
            page = urllib.urlopen(WebParser.requestURL, params)
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
        for i in xrange(len(self.webData)-3):
            if self.webData[i] == self.thisCourse.subject \
                    and self.webData[i+2] == self.thisCourse.catalogNumber:
                        self.index = i
                        break
        if self.index == -1:  # website not found
            return "CourseNotFound"

    def processCourseInfo(self):
        """now, we do the heavy-duty processing of the data table"""

        # sets basic attrs of thisCourse
        self.thisCourse.units = self.webData[self.index+4]
        self.thisCourse.title = self.webData[self.index+6]
        while self.webData[self.index] != "Instructor":
            self.index += 1

        # processing row-by-row
        while not self.endOfRow(self.webData[self.index]):
            if self.webData[self.index] != "":
                self.processSlot()
            self.index += 1
            if self.index == len(self.webData):
                return

    def processSlot(self):
        """we check to see if this is the BEGINNING of a valid row"""

        if (self.webData[self.index+1][:3].upper() == "LEC"
                or self.webData[self.index+1][:3].upper() == "LAB") \
                and "ONLINE" not in self.webData[self.index+2]:
            # we don't want online classes!
            # processing a lecture row
            lec = Lecture()
            if self.processClass(lec, self.index, self.webData):
                return
            self.thisCourse.lectures.append(lec)
        elif self.webData[self.index+1][:3].upper() == "TUT":
            # processing a tutorial row
            tut = Tutorial()
            if self.processClass(tut, self.index, self.webData):
                return
            self.thisCourse.tutorials.append(tut)
        elif self.webData[self.index][:7].upper() == "RESERVE":
            # processing a reserve row
            res = Reserve()
            self.processReserve(res, self.index, self.webData)
            if self.thisCourse.lectures:
                self.thisCourse.lectures[-1].reserves.append(res)
        # note: we leave out the TST (exam?) times for now

    def processReserve(self, res, index, webData):
        """processing reservations for certain types of students"""

        res.name = webData[index][9:]

        # we remove the "only" suffix (which is annoyingly pointless)
        if "only" in res.name:
            res.name = res.name[:-5]

        # also, the "students" suffx
        if "students" in res.name or "Students" in res.name:
            res.name = res.name[:-9]

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
        if not match:
            # we return an error message in the "TBA" case
            return "NoTimeError"

        attr3 = ["startTime", "endTime", "days"]
        for i in xrange(len(attr3)):
            setattr(lec, attr3[i], match.group(i+1).strip())
        index += 1

        if len(webData[index].split()) == 2:
            # sometimes, no building, room, and instructor will be given
            # this is mostly for Laurier courses
            lec.building, lec.room = webData[index].split()
            lec.instructor = webData[index+1].strip()

    def endOfRow(self, data):
        """returns true if the current data-cell is the last cell
        of this course; else - false"""

        # the last cell is of the form: ##/##-##/## or
        # "Information last updated
        if re.search(r"\d+/\d+-\d+/\d+", data) or \
                "Information last updated" in data:
            return True
        else:
            return False

    def postProcess(self, course):
        """this function will convert the class times to minutes-past-
        the-previous-midnight, and converts the days to numbers.
        Also, some reservation-postprocessing"""

        map(lambda x: x.calcMiscSeats(), course.lectures)
        for lec in course.lectures:
            lec.courseID = course.subject + " " + course.catalogNumber
        for tut in course.tutorials:
            tut.courseID = course.subject + " " + course.catalogNumber

        for slot in course.lectures + course.tutorials:
            # first, we convert time to 24hr time
            # earliest start time for a class is 8:30am
            # night classes start at/before 7:00pm
            if 1 <= int(slot.startTime.split(":")[0]) <= 7:
                slot.startTime, slot.endTime = \
                    map(lambda x: "{}:{}".format(str(int(x.split(":")[0])
                        + 12), x[-2:]), [slot.startTime,
                        slot.endTime])

            elif int(slot.startTime.split(":")[0]) > int(
                    slot.endTime.split(":")[0]):
                # e.g. 12:00 to 1:00
                slot.endTime = "{}:{}".format(str(int(
                    slot.endTime.split(":")[0])+12), slot.endTime[-2:])

            # now, we write to slot.sTime, slot.eTime
            # (minutes-past-midnight...)
            slot.sTime, slot.eTime = map(lambda x: int(x[:2]) * 60 +
                                         int(x[-2:]),
                                         [slot.startTime, slot.endTime])

            # we write to slot.ndays, where ndays is a string of numbers,
            # 0->4
            if "M" in slot.days:
                slot.ndays += "0"

            i = slot.days.find("T")
            if i != -1 and (i == len(slot.days) - 1 or
                            slot.days[i+1] != 'h'):
                # basically, if not Th (for Thursday)
                slot.ndays += "1"

            # now, for the rest of the days...
            for i in [("W", "2"), ("Th", "3"), ("F", "4")]:
                if i[0] in slot.days:
                    slot.ndays += i[1]

            # we make a small adjustment to campusLocation,
            # removing whitespace
            slot.campusLocation = slot.campusLocation.split()[0]

            # we make the prof name "first last" instead of
            # "last,first middle"

            if slot.instructor != "":
                s = slot.instructor.split(" ")
                for i in s:
                    if "," in i:
                        # we want the 2 words connected by the ","
                        slot.instructor = " ".join(reversed(list(
                            i.split(","))))
