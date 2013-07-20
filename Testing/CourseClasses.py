import re

class Slot:
	# the basic template containing fundamental attributes of a university class
	# named "Slot" to avoid confusing it with classes
	classNumber = ""
	compSec = ""	# short for "Component Section" (e.g. LEC 001)
	campusLocation = ""
	# assocClass, Rel1, Rel2 are left out for now (not very useful)
	enrlCap = 0
	enrlTotal = 0
	waitCap = 0
	waitTotal = 0
	days = "" # e.g. "MWF"
	startTime = ""
	endTime = ""
	building = ""
	room = ""
	instructor = ""

	def process(self, index, allData):
		# heavy-duty processing of the data array
		attr1 = ["classNumber", "compSec", "campusLocation"]
		for i in xrange(len(attr1)):
			setattr(self, attr1[i], allData[index+i])
		index += 5

		attr2 = ["enrlCap", "enrlTotal", "waitCap", "waitTotal"]
		for i in xrange(len(attr2)):
			setattr(self, attr2[i], int(allData[index+i]))
		index += 4

		#parsing the "Times Days/Date" field
		match = re.search(r'([:\d]+)-([:\d]+)(\w+)', allData[index])
		attr3 = ["startTime", "endTime", "days"]
		for i in xrange(len(attr3)):
			setattr(self, attr3[i], match.group(i+1))
		index += 1

		self.building, self.room = allData[index].split()
		self.instructor = allData[index+1]
		index += 2

		return index

class Reserve:
	names = [] # e.g. "AFM", "Math CA", etc.
	enrlCap = 0
	enrlTotal = 0

	def __init__(self, index, allData):
		reserveText = allData
		pass


class Lecture(Slot):
	reserves = []


class Tutorial(Slot):
	pass


class Course:
	subject = ""
	catalogNumber = ""
	units = ""
	title = ""
	lectures = []
	tutorials = []

	def __init__(self, queryString):
		self.subject = queryString.split()[0].upper().strip()
		self.catalogNumber = queryString.split()[1].strip()
	
	def processSlot(self, index, allData):
		if allData[index+1][:3].upper() == 'LEC':
			# print "Lecture!"
			lec = Lecture()
			index = lec.process(index, allData)
			self.lectures.append(lec)
			import pdb; pdb.set_trace()
		elif allData[index+1][:3].upper() == 'TUT':
			# print "Tutorial!"
			pass
		elif allData[index][:7].upper() == 'RESERVE':
			res = Reserve(index, allData)
			lectures[-1].reserves.append(res)
		return index
