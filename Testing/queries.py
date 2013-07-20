import urllib
import re
from HTMLParser import HTMLParser
from CourseClasses import * # all important classes

class Parser(HTMLParser):
	# this class parses the form
	# TODO: Add allData to this class, along with the following code
	def handle_data(self, data):
		allData.append(data.strip())

# some "global" variables
queryString = " afm 101"
tmp = Course(queryString)

# Decryption of the session id (1139): "1", 20"13" (year), "9"/fall (month)
session = "1139"
requestURL = "http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"

# each cell of information is an element of allData
allData = []


# now, passing the parameter to the POST form to obtain a html page, which we then parse
params = urllib.urlencode({'sess' : '1139', 'subject' : tmp.subject})
#params = urllib.urlencode({'sess' : '2320', 'subject' : 'AFM'}) # invalid session for testing

stream = urllib.urlopen(requestURL, params)

myParser = Parser()
myParser.feed(stream.read())

# TODO: the following code should be refactored

index = -1
for i in xrange(len(allData)-1):
	if allData[i] == tmp.subject and allData[i+1] == tmp.catalogNumber:
		index = i
		break

# TODO: deal with index == -1 (course not found)

# strangely, all tables end with a #/#-#/# thing (e.g. 10/17-10/17)
# not quite sure what that does, but regex should pick it up

def isEnd(data):
	if re.search(r'\d+/\d+-\d+/\d+', data):
		return True
	else:
		return False

tmp.units = allData[index+2]
tmp.title = allData[index+3]
while allData[index] != "Instructor":
	index += 1
index += 1

while isEnd(allData[index]) == False:
	if allData[index] == "":
		index += 1
		continue

	index = tmp.processSlot(index, allData)
	index += 1
