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
	time = "" # e.g. 08:30-09:20
	building = ""
	room = ""
	instructor = ""

class Reserve:
	names = [] # e.g. "AFM", "Math CA", etc.
	enrlCap = 0
	enrlTotal = 0

class Lecture(Slot):
	compSecNum = "" # component section number
	reserves = []

class Tutorial(Slot):
	compSecNum = "" # component section number

class Course:
	subject = ""
	catalogNumber = ""
	units = ""
	title = ""
	lectures = []
	tutorials = []
