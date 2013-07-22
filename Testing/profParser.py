import urllib
from webParser import CustomHTMLParser


class RateMyProfParser:
    """We will retrieve the attributes of the instructor"""

    # call str.format(last name, school id, pageNum)
    # OKAY, this search relies on the assumption that
    # the last name is unique enough to narrow profs down to ~10
    # which is the limit for a page
    requestURL = "http://www.ratemyprofessors.com/SelectTeacher.jsp" \
                 "?searchName={}&search_submit1=Search&sid={}&pageNo={}"

    def __init__(self, name, schoolID="1490"):  # professor's name
        # 1490 = Waterloo
        # TODO: look up some other schools' IDs?

        self.name = name.strip()
        self.schoolID = schoolID
        self.webData = []

    def getInfo(self):
        """will return (avgRating, numRatings) if exists.
        Else, return None"""

        if self.name == "":
            # lecture/tutorial has no name
            return

        # start at page 1
        pageNum = 1
        while pageNum <= 3:  # if there are 60 Wang's, for example, tough
            # two possible errors (page out of range, or website down)
            err = self.getWebData(pageNum)
            if err:
                return
            ret = self.parseWebData()
            if ret:
                # form of: (# ratings, overall quality, easiness)
                return ret
            else:
                self.webData = []  # clear the data
                pageNum += 1

    def getWebData(self, pageNum):
        """fetching data from the webpage"""
        try:
            URL = self.requestURL.format(self.name.split()[1],
                                         self.schoolID, str(pageNum))
            page = urllib.urlopen(URL)
            parser = CustomHTMLParser(self.webData)
            parser.feed(page.read().replace("&nbsp", " "))
            for data in self.webData:
                if "Invalid page number" in data or \
                        "didn't return any results for professors" in data:
                    # essentially, page out of range
                    return "InvalidPageError"
        except:
            return "WebPageError"

    def parseWebData(self):
        """parsing the webData list to get attrs"""
        """if we have the desirable attributes"""

        firstName, lastName = self.name.split()
        for i, data in enumerate(self.webData):
            if firstName in data and lastName in data:
                # we found it!
                return (int(self.webData[i+4]), float(self.webData[i+6]),
                        float(self.webData[i+8]))
