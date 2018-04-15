from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
import datetime

random.seed(datetime.datetime.now())


def getLinks(articleName):
    """Articlename should be a string."""
    html = urlopen("http://en.wikipedia.org"+articleName)
    bsObj = BeautifulSoup(html.read(), "html5lib")
    return bsObj.find("div", {"id": "bodyContent"}).findAll("a", {"href": re.compile("^(/wiki/)((?!:).)*$")})


links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
