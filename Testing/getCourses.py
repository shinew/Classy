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
    names = f.read().split()

requestURL = "http://www.adm.uwaterloo.ca/cgi-bin/" \
             "cgiwrap/infocour/salook.pl"

allIDs = []  # contains "AFM 101", "CS 145", etc.
for name in names:
    webData = []
    params = urllib.urlencode({"sess": "1139", "subject": name})
    page = urllib.urlopen(requestURL, params)
    parser = CustomHTMLParser(webData)
    parser.feed(page.read().replace("&nbsp", " "))
    for i, e in enumerate(webData):
        if e.strip().lower() == 'subject':
            allIDs.append(webData[i+9] + " " + webData[i+11])

# write to file
with open("allIDs.txt", "w") as f:
    for ID in allIDs:
        f.write(ID + "\n")
