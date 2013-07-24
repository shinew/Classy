"""
Copyright 2013 Shine Wang

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from webParser import WebParser
from courseClasses import Course


class Matcher:
    """This class will process the courses given, and (most likely) find
    an optimal schedule"""

    def __init__(self, courses):

        # the courses
        self.courses = courses
        self.numCourses = len(self.courses)

        # set of taken intervals
        self.timesOccupied = set()

        # indices of the course tutorial/lecture
        # -1 means not available
        self.tutIndices = [-1 for i in xrange(self.numCourses)]
        self.lecIndices = [-1 for i in xrange(self.numCourses)]

    def matching(self):
        """recursively finds the slots
        stop when it returns None"""
        return self.matchingLecture(0)

    def matchingTutorial(self, index):
        """we want to choose the best courses first, not tutorials"""
        if index == self.numCourses:
            yield self.getSlots()
        else:
            if len(self.courses[index].tutorials) == 0:
                self.tutIndices[index] = -1
                for y in self.matchingTutorial(index+1):
                    yield y
            else:
                for i, tut in enumerate(self.courses[index].tutorials):
                    times = self.notOccupied(tut)
                    if times:
                        self.tutIndices[index] = i
                        map(self.timesOccupied.add, times)
                        for y in self.matchingTutorial(index+1):
                            yield y
                        map(self.timesOccupied.remove, times)
                        self.tutIndices[index] = -1

    def matchingLecture(self, index):
        """very similar to tutorials - different base case"""
        if index == self.numCourses:
            for y in self.matchingTutorial(0):
                yield y
        else:
            if len(self.courses[index].lectures) == 0 or \
                    not filter(lambda x: x.thisUserCanAdd,
                            self.courses[index].lectures):
                    # either no lectures, or all lectures are full
                self.lecIndices[index] = -1
                for y in self.matchingLecture(index+1):
                    yield y
            else:
                for i, lec in enumerate(self.courses[index].lectures):
                    if not lec.thisUserCanAdd:
                        # this user can't use this slot
                        continue
                    times = self.notOccupied(lec)
                    if times:
                        self.lecIndices[index] = i
                        map(self.timesOccupied.add, times)
                        for y in self.matchingLecture(index+1):
                            yield y
                        map(self.timesOccupied.remove, times)
                        self.lecIndices[index] = -1

    def notOccupied(self, slot):
        """checks to see if the times are occupied already"""
        times = []
        for d in slot.ndays:
            times.append((slot.sTime + 24*60*int(d),
                         slot.eTime + 24*60*int(d)))

        for t in times:
            for j in self.timesOccupied:
                # <= instead of < because we don't want adjacent classes
                if j[0] <= t[0] <= j[1] or j[0] <= t[1] <= j[1]:
                    return False
        return times

    def getSlots(self):
        """returns the slots"""
        ret = []
        for i, e in enumerate(self.lecIndices):
            if e != -1:
                ret.append(self.courses[i].lectures[e])
        for i, e in enumerate(self.tutIndices):
            if e != -1:
                ret.append(self.courses[i].tutorials[e])
        return ret
