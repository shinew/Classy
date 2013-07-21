from webParser import WebParser
from courseClasses import Course

class Matcher:
    """This class will process the courses given, and hopefully find
    an optimal schedule"""

    def __init__(self, courses):

        # list of courses
        self.courses = courses
        self.numCourses = len(self.courses)
        # list of tuples, containing (startTime, endTime) relative to
        # the midnight between Sunday-Monday
        self.timesTaken = []

        # list of the lectures and tutorial times selected
        # indexing will be: 0..N-1 = Course-->Lecture
        # N..2N-1 = Course-->Tutorial
        # elements would be index of the lecture
        self.selection = []

    def matching(self, index=0):

        # end of recursion, we matched everything
        #if index == 2 * self.numCourses:
        if index == 2*self.numCourses:
            final = []
            for i,e in enumerate(self.selection[:self.numCourses]):
                if e != -1:
                    final.append(self.courses[i].lectures[e])
            for i,e in enumerate(self.selection[self.numCourses:]):
                if e != -1:
                    final.append(self.courses[i].tutorials[e])
            #for i,e in enumerate(self.selection[self.numCourses:]):
            #    final.append(self.courses[i].tutorials[e])
            return final

        times = 0 # number of days in the selected lecture

        if index < self.numCourses:
            # a lecture
            times = self.matchProcessing(index, "lectures")
            if not times:
                return #this course is impossible
        else:
            # a tutorial
            times = self.matchProcessing(index-self.numCourses, "tutorials")
            if not times:
                return

        ret = self.matching(index+1)
        if ret:
            return ret
        else:
            # error found before, we remove times
            # from the timesTaken stack
            if times != -1:
                for i in xrange(times):
                    self.timesTaken.pop()
            self.selection.pop()
        
    def matchProcessing(self, index, slotType):
        """we try to find an appropriate slot for this course and type"""
        """returns the # of days in this slot if found; else None"""
        """if no tutorial, we return -1"""
        # we make sure no time conflicts exist
        if len(getattr(self.courses[index], slotType)) == 0:
            # if no tutorial, we ADD TO SELECTION, but not to timesTaken
            self.selection.append(-1)
            return -1

        for slotIndex, slot in enumerate(getattr(self.courses[index], slotType)):
            times = []
            for d in slot.ndays:
                times.append( (slot.sTime + 24*60*int(d),
                        slot.eTime + 24*60*int(d))   )

            # make sure not taken already
            isBad = False
            for t in times:
                if isBad:
                    break
                for j in self.timesTaken:
                    # <= becaus we don't want adjacent classes
                    if j[0] <= t[0] <= j[1] or j[0] <= t[1] <= j[1]:
                        isBad = True
                        break

            if isBad:
                continue

            self.timesTaken.extend(times)
            self.selection.append(slotIndex)
            return len(times)
        return
