class Slot(object):
    """the basic template containing fundamental attributes of a
    university class. It is named "Slot" to avoid confusing it
    with classes"""

    def __init__(self):
        self.classNumber = ""
        self.compSec = ""    # short for "Component Section" (e.g. LEC 001)
        self.campusLocation = ""

        # assocClass, Rel1, Rel2 are left out for now (not very useful)
        self.enrlCap = 0
        self.enrlTotal = 0
        self.waitCap = 0
        self.waitTotal = 0
        self.days = ""  # e.g. "MWF"
        self.sTime = 0  # minutes past midnight (00:00)
        self.eTime = 0
        self.ndays = ""
        self.startTime = ""
        self.endTime = ""
        self.building = ""
        self.room = ""

        # some attributes associated with the prof
        self.instructor = ""
        self.numRatings = 0
        self.quality = 0.0
        self.easiness = 0.0

    def __str__(self):
        attrs = ["classNumber", "compSec", "campusLocation", "startTime", "endTime", "days", "building", "room", "instructor"]
        return "\t".join(map(str, [getattr(self, x) for x in attrs]))

    def __repr__(self):
        attrs = ["classNumber", "compSec", "campusLocation", "enrlCap",
                 "enrlTotal", "waitCap", "waitTotal", "days",
                 "startTime", "endTime", "building", "room", "instructor",
                 "numRatings", "quality", "easiness"]
        return "*".join(map(str, [getattr(self, x) for x in attrs]))


class Reserve:
    """A "reservation" made for certain types of students"""

    def __init__(self):
        self.names = []  # e.g. "AFM", "Math CA", etc.
        self.enrlCap = 0
        self.enrlTotal = 0

    def __repr__(self):
        return "*".join(self.names) + "*" + str(self.enrlCap) + \
               "*" + str(self.enrlTotal)


class Lecture(Slot):
    """One "lecture" slot"""
    def __init__(self):
        super(Lecture, self).__init__()
        self.reserves = []


class Tutorial(Slot):
    """One "tutorial" slot"""
    pass


class Course:
    """represents a "course" e.g. AFM 101, ECON 101"""

    def __init__(self, session, queryString):
        """processing the queryString e.g. 'afm 101' """

        self.session = session.strip()
        self.subject = queryString.split()[0].upper()  # e.g. AFM
        self.catalogNumber = queryString.split()[1]  # e.g. 101
        self.units = ""
        self.title = ""
        self.lectures = []
        self.tutorials = []
