from assignment import *
from activity import *
from datetime import *
from pytz import timezone

class Scheduler:

    def __init__(self, activities=[], assignments=[]):
        self.activities = activities
        self.assignments = assignments
        
    def createAssignment(self, newAssignment):
        self.assignments.append(newAssignment)
    
    def createActivity(self, newActivity):
        self.activities.append(newActivity)
        
    def newActivity(self, name, start, length, description):        
        activity = Activity(name, start, length, description)
        self.createActivity(activity)
        
    def newAssignment(self, name, start, length, due, description, links):
        assignment = Assignment(name, start, length, due, description, links)
        self.createAssignment(assignment)

    def compileSchedule(self, BREAK_TIME):

        #print("Test Compile")
    
        #Sort all the activities and assignments
        self.activities.sort(key=lambda x: x.start)
        self.assignments.sort(key=lambda x: x.due)

        #Get the current Time
        timeNow = datetime.now(timezone('UTC'))
        timeNow -= timedelta(hours=5)
        #print("Time Now:")
        #print(datetime.now())

        #Remove all activities that are before the current time
        '''
        toRemove = []

        for actInd in range(len(self.activities)):
            curAct = self.activities[actInd]
            if curAct.start + curAct.length < timeNow:
                toRemove.append(actInd)

        for removeInd in sorted(toRemove, reverse=True):
            self.activities.pop(removeInd)

        #print(self.activities)

        #Remove all the assignments that are due before the current time
        toRemove = []

        for actInd in range(len(self.assignments)):
            curAct = self.assignments[actInd]
            if curAct.due < timeNow:
                toRemove.append(actInd)

        for removeInd in sorted(toRemove, reverse=True):
            self.assignments.pop(removeInd)

        #print(self.assignments)

        '''

        #Get all the time intervals 
        timeIntervals = []

        for acti in self.activities:
            timeIntervals.append([acti.start, acti.start + acti.length])

        #print(timeIntervals)

        #Loop through each Assignment

        #print("First Time Interval")
        #print(timeIntervals)

        assignmentTimes = []

        for assign in self.assignments:
            #print(assign)
            #First check if the very first position works
            if assign.start + assign.length + BREAK_TIME <= timeIntervals[0][0]:
                assignmentTimes.append([assign, assign.start])
                timeIntervals.insert(0, [assign.start, assign.start + assign.length])
                #print(timeIntervals)
                continue

            #Check every beginning and end of each time interval

            #Keep track of the end time of the previous interval
            lastTime = timeIntervals[0][1]

            #Skip the First Interval
            firstIter = True

            #Check if we assigned it when the loop is over
            assignCheck = False

            counter = 0

            for timeInt in timeIntervals:
                counter += 1

                if firstIter:
                    firstIter = False
                    continue


                if lastTime + BREAK_TIME + assign.length > assign.due:
                    return f'Error,{assign.name}'

                if lastTime + BREAK_TIME + assign.length + BREAK_TIME <= timeInt[0]:
                    assignCheck = True
                    assignmentTimes.append([assign, lastTime + BREAK_TIME])
                    timeIntervals.insert(counter, [lastTime + BREAK_TIME, lastTime + BREAK_TIME + assign.length])
                    #print(timeIntervals)
                    break

                lastTime = timeInt[1]

            if assignCheck:
                continue

            #Check the very last interval
            lastInt = timeIntervals[-1]

            if lastInt[1] + BREAK_TIME + assign.length > assign.due:
                return f'Error,{assign.name}'

            if lastInt[1] + BREAK_TIME + assign.length < assign.due:
                assignmentTimes.append([assign, lastInt[1] + BREAK_TIME])
                timeIntervals.append([lastInt[1] + BREAK_TIME, lastInt[1] + BREAK_TIME + assign.length])

        #for assign in assignmentTimes:
        #    print(f'{assign[0].name} assigned at {assign[1]}')

        #Intertwine the Activities with the Assignments

        allTimes = []

        curPointer = 0

        for acti in self.activities:
            if len(assignmentTimes) == 0 or curPointer == len(assignmentTimes):
                allTimes.append([acti, acti.start])
                continue

            if acti.start < assignmentTimes[curPointer][1]:
                allTimes.append([acti, acti.start])
            else:
                allTimes.append(assignmentTimes[curPointer])
                curPointer += 1

        while curPointer < len(assignmentTimes):
            allTimes.append(assignmentTimes[curPointer])
            curPointer += 1

        return allTimes

    
"""
        testScheduler = Scheduler()

        #Activity that starts on Feb 19 10:30 and lasts 30 minutes
        activity1 = Activity("Activity 1", datetime(2022,2,19,11,0), timedelta(minutes=60), "Activity 1 Description")

        #Activity that will be automatically removed
        #activity2 = Activity("Activity 2", datetime(8,1,1), timedelta(minutes=30), "Activity 2 Description")

        #Another Activity that starts on Feb 20 4:30 am and lasts 2 hours
        #activity3 = Activity("Activity 3", datetime(2022, 2, 20, 4, 30), timedelta(hours=30), "Activity 3 Description")

        testScheduler.createActivity(activity1)
        #testScheduler.createActivity(activity2)
        #testScheduler.createActivity(activity3)

        #Assignment that takes 30 minutes and is due at 2/18 11:59pm
        assignment1 = Assignment("Assignment 1", datetime.now(), timedelta(minutes=30), datetime(2022,2,19,11,0), "Assignent 1 Description")

        assignment2 = Assignment("Assignment 2", datetime.now(), timedelta(minutes=30), datetime(2022,2,19,22,59), "Assignment 2 Description")

        testScheduler.createAssignment(assignment1)
        testScheduler.createAssignment(assignment2)

        testSchedule = testScheduler.compileSchedule(timedelta(minutes=10))

        #print(testSchedule)
"""