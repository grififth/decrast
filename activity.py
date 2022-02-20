import textwrap

class Activity:
    def __init__(self, name, start, length, description):
        self.name = name #Name value
        self.start = start #Datetime value
        self.length = length #Timedelta value
        self.description = description #Description value

    def __repr__(self):
        informationArray = []
        
        informationArray.append(self.name)
        informationArray.append("")
        informationArray.append("Start")
        informationArray.append(self.start.strftime("%a %b %d %Y %I:%M %p"))
        informationArray.append("")
        informationArray.append("End")
        informationArray.append((self.length+self.start).strftime("%a %b %d %Y %I:%M %p"))
        
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

        return bordertop+'\n'+'\n'.join(informationArray)+borderbottom