from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html.read(), "html5lib")

tr = bsObj.findAll("tr", {"class": "gift", "id": "gift3"})
clas = bsObj.img.attrs["src"]
print(clas)
