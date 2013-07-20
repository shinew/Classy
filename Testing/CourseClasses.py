import re

class Slot:
    # the basic template containing fundamental attributes of a university class
    # named "Slot" to avoid confusing it with classes
    classNumber = ""
    compSec = ""    # short for "Component Section" (e.g. LEC 001)
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

    def __repr__(self):
        attrs = ["classNumber", "compSec", "campusLocation", "enrlCap", "enrlTotal", "waitCap", "waitTotal", "days", "startTime", "endTime", "building", "room", "instructor"]
        return "*".join(map(str, [getattr(self, x) for x in attrs]))

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

        # parsing the "Times Days/Date" field
        match = re.search(r'([:\d]+)-([:\d]+)(\w+)', allData[index])
        attr3 = ["startTime", "endTime", "days"]
        for i in xrange(len(attr3)):
            setattr(self, attr3[i], match.group(i+1))
        index += 1

        self.building, self.room = allData[index].split()
        self.instructor = allData[index+1]

        return index

class Reserve:
    names = [] # e.g. "AFM", "Math CA", etc.
    enrlCap = 0
    enrlTotal = 0

    def __init__(self, index, allData):
        # warning: we merge the next 4 cells together, because the text is split between them
        reserveText = "".join(allData[index:index+3])
        #print reserveText

        # we leave out the first match, because it is the word "reserve"
        self.names = map(lambda x: x.strip(), re.findall(r'[\w\d\s\-\/]+', reserveText)[1:])

        # we remove the "only" suffix
        if "only" in self.names[-1]:
            self.names[-1] = self.names[:-5]

        # now, we merge the match list
        while not allData[index].isdigit():
            index += 1
        self.enrlCap = int(allData[index])
        self.enrlTot = int(allData[index+1])
        index += 4

        pass

    def __repr__(self):
        return "*".join(self.names) + "*" + str(self.enrlCap) + "*" + str(self.enrlTotal)

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
            # processing a lecture row
            lec = Lecture()
            index = lec.process(index, allData)
            self.lectures.append(lec)
        elif allData[index+1][:3].upper() == 'TUT':
            # processing a tutorial row
            tut = Tutorial()
            index = tut.process(index, allData)
            self.tutorials.append(tut)
        elif allData[index][:7].upper() == 'RESERVE':
            # processing a reserve row
            res = Reserve(index, allData)
            self.lectures[-1].reserves.append(res)
        # note: we leave out the TST (exam?) times for now
        return index
