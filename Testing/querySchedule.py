import urllib
params = urllib.urlencode({'sess' : '1139', 'subject' : 'AFM'})
f = urllib.urlopen("http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl", params)
print f.read() #this now primts the AFM page for the Fall 2013 session
