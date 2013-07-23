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
from HTMLParser import HTMLParser


class CustomHTMLParser(HTMLParser):
    """this class reads a HTML stream, then parses out the "data" fields"""

    def __init__(self, webData):
        HTMLParser.__init__(self)
        self.webData = webData

    def handle_data(self, data):
        """takes out the data"""
        self.webData.append(data.strip())

names = []  # contains "AFM", "CS", etc.
with open("names.txt", "r") as f:
    # the names.txt contains all the possible prefixes like AFM, CS, etc.
    names = f.read().split()

requestURL = "http://www.adm.uwaterloo.ca/cgi-bin/" \
             "cgiwrap/infocour/salook.pl"

allIDs = []  # contains "AFM 101", "CS 145", etc.
for name in names:
    print "Currently doing", name + "..."
    webData = []
    params = urllib.urlencode({"sess": "1139", "subject": name})
    page = urllib.urlopen(requestURL, params)
    parser = CustomHTMLParser(webData)
    parser.feed(page.read().replace("&nbsp", " "))
    for i, e in enumerate(webData):
        if e.strip().lower() == 'subject':
            allIDs.append(webData[i+9] + " " + webData[i+11])

# write to file
with open("allIDs", "w") as f:
    for ID in allIDs:
        f.write(ID + "\n")
