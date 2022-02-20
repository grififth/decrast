from scheduler import *
from imports import *
from scraper import Scraper
from pytz import timezone

logoASCII = """\033[1;96m
      d8b                                                  
      88P                                             d8P  
     d88                                           d888888P
 d888888   d8888b d8888b  88bd88b d888b8b   .d888b,  ?88'  
d8P' ?88  d8b_,dPd8P' `P  88P'  `d8P' ?88   ?8b,     88P   
88b  ,88b 88b    88b     d88     88b  ,88b    `?8b   88b   
`ඞ88P'`88b`?888P'`?888P'd88'     `?88P'`88b`?888P'   `?8b

     Your Best Friend for Stopping Procrastination\033[0;49m"""

help = """
\033[1;91m➢  (1) Create an Activity
➢  (2) Create an Assignment
➢  (3) Display current schedule
➢  (4) Import calendar from Imports folder
➢  (5) Exports scheduling interface to Exports folder
➢  (6) Quick Search
➢  (7) Exit\033[0;49m
"""

if __name__ == "__main__":
    
    print(logoASCII)
    
    schedule = Scheduler()
    scraper = Scraper()

    #sactivity = Activity("Swimming Practice", datetime(2022,5,20,11,0), timedelta(minutes=30), "sasda")
    #sassignments = Assignment("do ur mom", datetime(2022,5,20,11,0), timedelta(minutes=30), datetime(2022,5,20,14,0), "gaming bedwars minecraft sheesh amongus3amgonewrong", ["hi.com"])
    #schedule.createActivity(sactivity)
    #schedule.createAssignment(sassignments)

    while True:
        
        print(help)
        
        prompt = "\033[3;35mAction >>\033[0;35m"
        print(prompt, end=' ')
        action = input()
        print("\033[0;49m", end="")

        if action=="1":
            print("\033[3;35mActivity Name? >>\033[0;35m", end=' ')
            name = input()
            
            print("\033[3;35mStart Time? (YEAR-MONTH-DAY-HOUR-MINUTE) >>\033[0;35m", end=' ')
            start = datetime(*list(map(int,input().split('-'))))
            start = start.replace(tzinfo=timezone("UTC"))
            
            print("\033[3;35mLength? (DAYS-HOURS-MINUTES) >>\033[0;35m", end=' ')
            times = list(map(int,input().split('-')))
            length = timedelta(
                days = times[0],
                hours = times[1],
                minutes = times[2]
            )
            
            print("\033[3;35mDescription? >>\033[0;35m", end=' ')
            description = input()
            
            schedule.newActivity(name, start, length, description)

            print("\n\033[92m✓ Succesfully Created a new Activity! ✓\033[92m")
            
        elif action=="2":
            print("\033[3;35mAssignment Name? >>\033[0;35m", end=' ')
            name = input()
            
            print("\033[3;35mStart Time? (YEAR-MONTH-DAY-HOUR-MINUTE) >>\033[0;35m", end=' ')
            start = datetime(*list(map(int,input().split('-'))))
            start = start.replace(tzinfo=timezone("UTC"))
            
            print("\033[3;35mLength (DAYS-HOURS-MINUTES) >>\033[0;35m", end=' ')
            times = list(map(int,input().split('-')))
            length = timedelta(
                days = times[0],
                hours = times[1],
                minutes = times[2]
            )
            
            print("\033[3;35mDue Date? (YEAR-MONTH-DAY-HOUR-MINUTE) >>\033[0;35m", end=' ')
            due = datetime(*list(map(int,input().split('-'))))
            due = due.replace(tzinfo=timezone("UTC"))
            
            print("\033[3;35mDescription? >>\033[0;35m", end=' ')
            description = input()

            print("\033[3;35mDo you wish to automatically search for related links? (y/n) >>\033[0;35m", end=' ')
            ifGate = input().lower()

            links = []

            if 'n' not in ifGate:
                print("\033[3;35mWhat do you want to search for? >>\033[0;35m", end=' ')
                searchPhrase = input()

                links = scraper.scrape(searchPhrase, 5)

                print(f'\033[3;96mWe found {len(links)} results.\n')

                for searchResult in links:
                    print(f'\033[0;96m{searchResult}\033[1;49m')

            totalResults = []
            
            schedule.newAssignment(name, start, length, due, description, links)

            print("\n\033[92m✓ Succesfully Created a new Assignment! ✓\033[92m")
            
        elif action=="3":
            print("\033[3;35mBreak Time? (MINUTES) >>\033[0;35m", end=' ')
            bt = timedelta(minutes=int(input()))
            listTimes = schedule.compileSchedule(bt)
            
            for event in listTimes:
                if isinstance(event[0], Assignment):
                    event[0].start = event[1]
                    print("\033[1;91m")
                    print(event[0])
                    print("\033[1;49m")
                else:
                    print("\033[1;93m")
                    print(event[0])
                    print("\033[1;49m")
            
        elif action=="4":

            folders = os.listdir("./Imports")
            files=[]
            for num in range(len(folders)):
                f = f"({str(num+1)}) /Imports/{folders[num]}"
                files.append(f)
            
            mlen = len(max(files, key=len)) + 2
            
            print("\033[1;93m")

            bordertop = '\n┏' + '━' * (mlen) + '┓'
            #header = '┃' + ((mlen-15)//2)*" " + "Available Folders" + ((mlen-15)//2+(mlen-15)%2)*" " + '┃'
            header = '┃' + ('{:^' + str(mlen) + '}').format("Available Folders") + '┃'
            print(bordertop + "\n" + header)
            
            for file in files:
                #print('\033[1;93m┃' + ((mlen+2-len(file))//2)*" " + file + ((mlen+2-len(file))//2+(mlen+2-len(file))%2)*" " + '┃')
                print('┃' + ('{:^' + str(mlen) + '}').format(file) + '┃')
            
            borderbottom = '┗' + '━' * (mlen) + '┛'
            print(borderbottom)

            print("\033[0;49m")
            
            print("\033[3;35mFolder to Import Number >>\033[0;35m", end=' ')
            folder = folders[int(input())-1]
            unzipfile(folder)
            parse("./Calendars", schedule)
            print("\n\033[92m✓ Import Complete! ✓\033[92m")
            
        elif action=="5":
            print("\033[3;35mFilename to save schedule? >>\033[0;35m", end=' ')
            filename = input()
            print("\033[3;35mBreak time? >>\033[0;35m", end=' ')
            bt = int(input())
            unparse("./Exports", schedule, filename+'.ics', bt)
            print(f"\n\033[92m✓ Export to {filename}.ics complete! ✓\033[92m")
        elif action=="6":
            print("\033[3;35mWhat do you want to search for? >>\033[0;35m", end=' ')
            searchPhrase = input()

            print("\033[3;35mAt most how many results do you want? >>\033[0;35m", end=' ')
            results = int(input())

            searchResults = scraper.scrape(searchPhrase, results)

            print(f'\033[3;96mWe found {len(searchResults)} results.\n')

            for searchResult in searchResults:
                print(f'\033[0;96m{searchResult}\033[1;49m')
            
        elif action=="7":
            print("\n\033[1;96mThank you for using decrast. Good luck on your assignments!\033[0;49m")
            break
        else:
            print("\n\033[1;4;31m⚠  Invalid Input, please enter a number from 1-6. ⚠ \033[0;49m")