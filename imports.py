from icalendar import Calendar, Event, vCalAddress, vText
from pytz import timezone
from pathlib import Path
from assignment import *
from activity import *
import os
import zipfile
from datetime import *

def unzipfile(zipname):
    with zipfile.ZipFile("./Imports/" + zipname,"r") as zip_ref:
        zip_ref.extractall("./Calendars")

def parse(path, schedule):
    #open file representing full google calenders
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            g = open(f,'rb')
            gcal = Calendar.from_ical(g.read()) 
            #iterate through activities in google calender
            for component in gcal.walk():
                if component.name == "VEVENT":     
                    #create activity object and add to schedule object
                    summary = component.get('summary')
                    dtstart = component.get('dtstart').dt
                    dtend = component.get('dtend').dt
                    dtstart -= timedelta(hours=5)
                    dtend -= timedelta(hours=5)

                    '''
                    if isinstance(dtstart, date):
                        dtstart = datetime(dtstart.year, dtstart.month, dtstart.day)
                    if isinstance(dtend, date):
                        dtend = datetime(dtend.year, dtend.month, dtend.day)
                    '''
                    description = component.get('description')
                    act = Activity(summary, dtstart, dtend-dtstart, description)
                    schedule.activities.append(act)
            g.close()
            
def unparse(path, schedule, filename, breaktime):
    cal = Calendar()
    
    lst = schedule.compileSchedule(timedelta(minutes=breaktime))
    
    #add activities to calender object
    for activity, start in lst:

        if isinstance(activity, Activity):
            continue
    
        event = Event()
        event.add('summary', activity.name)
        event.add('dtstart', start + timedelta(hours=5))
        event.add('dtend', activity.start+activity.length + timedelta(hours=5))
        event.add('description', activity.description)
        
        """organizer = vCalAddress('MAILTO:hello@example.com')
        organizer.params['cn'] = vText('Sir Jon')
        organizer.params['role'] = vText('CEO')
        event['organizer'] = organizer
        event['location'] = vText('London, UK')"""
        
        # Adding events to calendar
        cal.add_component(event)
        
    """
    #add assignments to calender object
    for assignment in schedule.assignments:
        
        event = Event()
        event.add('summary', assignment.name)
        event.add('dtstart', assignment.start)
        event.add('dtend', assignment.start+assignment.length)
        event.add('description', activity.description)

        # Adding events to calendar
        cal.add_component(event)
    """

    #export calender object as icalendar
    f = open(os.path.join(path, filename), 'wb')
    f.write(cal.to_ical())
    f.close()