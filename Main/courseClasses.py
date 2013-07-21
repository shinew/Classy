class Slot:
    """the basic template containing fundamental attributes of a
    university class. It is named "Slot" to avoid confusing it
    with classes"""
    classNumber = ""
    compSec = ""    # short for "Component Section" (e.g. LEC 001)
    campusLocation = ""
    # assocClass, Rel1, Rel2 are left out for now (not very useful)
    enrlCap = 0
    enrlTotal = 0
    waitCap = 0
    waitTotal = 0
    days = "" # e.g. "MWF"
    sTime = 0 # minutes past midnight (00:00)
    eTime = 0
    ndays = ""

    startTime = ""
    endTime = ""
    building = ""
    room = ""
    instructor = ""

    def __repr__(self):
        # TODO: improve the formatting
        attrs = ["classNumber", "compSec", "campusLocation", "enrlCap",
                "enrlTotal", "waitCap", "waitTotal", "days",
                "startTime", "endTime", "building", "room", "instructor"]
        return "*".join(map(str, [getattr(self, x) for x in attrs]))

class Reserve:
    """A "reservation" made for certain types of students"""

    names = [] # e.g. "AFM", "Math CA", etc.
    enrlCap = 0
    enrlTotal = 0

    def __repr__(self):
        return "*".join(self.names) + "*" + str(self.enrlCap) + \
                "*" + str(self.enrlTotal)

class Lecture(Slot):
    reserves = []


class Tutorial(Slot):
    pass

class Course:
    """represents a "course" e.g. AFM 101, ECON 101"""

    session = ""
    subject = ""
    catalogNumber = ""
    units = ""
    title = ""
    lectures = []
    tutorials = []

    def __init__(self, session, queryString):
        """processing the queryString e.g. 'afm 101' """
        self.session = session.strip()
        self.subject = queryString.split()[0].upper().strip()
        self.catalogNumber = queryString.split()[1].strip()
