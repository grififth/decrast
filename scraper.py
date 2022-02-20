import requests
import re
from bs4 import BeautifulSoup
import random

class Scraper:
    def __init__(self):
        pass
    def scrape(self, keyword:str, results:int):
        words = keyword.split(" ")
        search = "+".join(words)
        page = requests.get(f"https://www.google.com/search?q={search}&num={results}")
        soup = BeautifulSoup(page.content, "html5lib")
        links = soup.findAll("a", {"class": "result__a"})

        #whitelisted "educational" apps
        whitelist = ["wikipedia.org", "britannica.org", "khanacademy.org", "3schools.com", "tutorialspoint.com", "sparknotes.com", "quora.com", "stackoverflow.com", "stackexchange.com", "calculatorsoup.com", "mathisfun.com", "wolframalpha.com", "history.com", "musictheory.net", "freecodecamp.org", "code.org", ".edu", ".gov"]


        final = []
        for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            actLink = link['href']
            for i in whitelist:
                if i in actLink:
                    final.append(actLink.split("&")[0][7:])

        random.shuffle(final)
        return final[:results]

if __name__ == "__main__":
    testScraper = Scraper()

    print(testScraper.scrape("calculus", 4))