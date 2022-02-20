import textwrap

class Assignment:
    def __init__(self, name, start, length, due, description, links=[]):
        self.start = start #Datetime object
        self.length = length #Timedelta object
        self.due = due #Datetime object
        self.name = name #Name of Assignment
        self.description = description
        self.links = links

    def __repr__(self):
        
        informationArray = []
        
        informationArray.append(self.name)
        informationArray.append("")
        informationArray.append("Start")
        informationArray.append(self.start.strftime("%a %b %d %Y %I:%M %p"))
        informationArray.append("")
        informationArray.append("Length")
        informationArray.append(':'.join(str(self.length).split(':')[:2]))
        informationArray.append("")
        informationArray.append("Due Date")
        informationArray.append(self.due.strftime("%a %b %d %Y %I:%M %p"))
        
        mlen = len(max(informationArray, key=len))
        
        wrapper = textwrap.TextWrapper(width=mlen)
        for line in self.description.split("\n"):
            informationArray.append(" ")
            for subline in wrapper.wrap(text=line):
                informationArray.append(subline)
                
        bordertop = '\n┏' + '━' * (mlen+2) + '┓'
        
        spaceF = lambda i: ((mlen-len(informationArray[i]))//2)*" "
        spaceB = lambda i: ((mlen-len(informationArray[i]))//2 + (mlen-len(informationArray[i]))%2)*" "
        
        for i in range(len(informationArray)):
            
            informationArray[i] = '┃ ' + spaceF(i) + informationArray[i] + spaceB(i) + ' ┃'
        
        borderbottom = '\n┗' + '━' * (mlen+2) + '┛'

        linkArray = ["Links"]

        for linkI in self.links:
            linkArray.append(linkI)

        llen = len(max(linkArray, key=len))

        lbordertop = '\n┏' + '━' * (llen+2) + '┓'
        
        for i in range(len(linkArray)):
            
            linkArray[i] = '┃ ' + ('{:^' + str(llen) + '}').format(linkArray[i]) + ' ┃'
        
        lborderbottom = '\n┗' + '━' * (llen+2) + '┛'
        
        if len(self.links) == 0:
            return bordertop+'\n'+'\n'.join(informationArray)+borderbottom
        else:
            return bordertop+'\n'+'\n'.join(informationArray)+borderbottom+'\n\033[1;96m'+lbordertop+'\n'+'\n'.join(linkArray)+lborderbottom+'\033[1;95m'