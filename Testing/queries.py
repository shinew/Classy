import urllib
from HTMLParser import HTMLParser

allData = []
class MyHTMLParser(HTMLParser):
	def handle_data(self, data):
		if len(data.strip()) != 0:
			allData.append(data.strip())

params = urllib.urlencode({'sess' : '1139', 'subject' : 'AFM'})
#params = urllib.urlencode({'sess' : '2320', 'subject' : 'AFM'})

f = urllib.urlopen("http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl", params)
htm = f.read() #htm contains the Accounting (AFM) courses for the Fall 2013 (1139) session

parser = MyHTMLParser()
parser.feed(htm)
