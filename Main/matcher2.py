from webParser import WebParser
from courseClasses import Course

class Matcher:
    """This class will process the courses given, and hopefully find
    an optimal schedule"""

    def __init__(self, courses):

        self.courses = courses
        self.numCourses = len(self.courses)
        self.timesTaken = {}

        self.tutIndices = [-1 for i in xrange(self.numCourses)]
        self.lecIndices = [-1 for i in xrange(self.numCourses)]

    def matching(self):
        return self.matchingTutorial(0)
    
    def matchingTutorial(self, index):
        if index == self.numCourses:
            for y in matchingLecture(0):
                yield y
        else: 
            if len(self.courses[index].tutorials) == 0:
                self.tutIndices[index] = -1
                for y in matchingTutorial(index+1):
                    yield y
            else:
                for i,tut in enumerate(self.courses[index].tutorials):
                    times = self.notOccupied(tut)
                    if times:
                        self.tutIndices[index] = i
                        map(self.timesTaken.add, times)
                        for y in matchingTutorial(index+1):
                            yield y
                        map(self.timesTaken.remove, times)
                        self.tutIndices[index] = -1

    def matchingLecture(self, index):
        if index == self.numCourses:
            yield self.getSlots()
        else: 
            if len(self.courses[index].tutorials) == 0:
                self.lecIndices[index] = -1
                for y in matchingLecture(index+1):
                    yield y
            else:
                for i,tut in enumerate(self.courses[index].tutorials):
                    times = self.notOccupied(tut)
                    if times:
                        self.lecIndices[index] = i
                        map(self.timesTaken.add, times)
                        for y in matchingLecture(index+1):
                            yield y
                        map(self.timesTaken.remove, times)
                        self.lecIndices[index] = -1

    def notOccupied(self, slot):
        times = []
        for d in slot.ndays:
            times.append( (slot.sTime + 24*60*int(d),
                    slot.eTime + 24*60*int(d))   )

        for t in times:
            for j in self.timesTaken:
                # <= becaus we don't want adjacent classes
                if j[0] <= t[0] <= j[1] or j[0] <= t[1] <= j[1]:
                    return False
        return times

    def getSlots(self):
        ret = []
        for i,e in self.lecIndices:
            if e != -1:
                ret.append(self.courses[i].lectures[e])
        for i,e in self.tutIndices:
            if e != -1:
                ret.append(self.courses[i].tutorials[e])
        return ret
