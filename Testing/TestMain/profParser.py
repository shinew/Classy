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
from webParser import CustomHTMLParser


class RateMyProfParser:
    """We will retrieve the attributes of the instructor"""

    # call str.format(last name, school id, pageNum)
    # OKAY, this search relies on the assumption that
    # the last name is unique enough to narrow profs down to ~10
    # which is the limit for a page
    requestURL = "http://www.ratemyprofessors.com/SelectTeacher.jsp" \
                 "?searchName={}&search_submit1=Search&sid={}&pageNo={}"
    cacheFile = "teacherCache.txt"
    cache = {}
    gotCache = False

    def __init__(self, name, schoolID="1490"):  # professor's name
        # 1490 = Waterloo
        # TODO: look up some other schools' IDs?

        self.name = name.strip()
        self.schoolID = schoolID
        self.webData = []

    def getCache(self):
        """get values of teacher cache"""
        if self.gotCache:
            # we only want to read the file once
            return
        self.gotCache = True
        try:
            # file data stored in standard "key\nvalue\n" format
            with open(self.cacheFile, "r") as f:
                name = f.readline().strip()
                while name:
                    self.cache[name] = eval(f.readline().strip())
                    name = f.readline().strip()
        except:
            return

    def getInfo(self):
        """will return (avgRating, numRatings) if exists.
        Else, return None"""

        # get cache names (if they exist)
        self.getCache()
        if self.name in self.cache:
            return self.cache[self.name]

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
                with open(self.cacheFile, "a") as f:
                    f.write(self.name + "\n")
                    f.write(str(ret) + "\n")
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
