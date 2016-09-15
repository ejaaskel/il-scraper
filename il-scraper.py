import requests
import time, threading
from bs4 import BeautifulSoup

titles = []

def scanNews():
	r = requests.get("http://www.iltalehti.fi")
	soup = BeautifulSoup(r.content)
	soupDiv = BeautifulSoup(str(soup.find("div", {"id": "iltab_luetuimmat-kaikki2"})))
	currentScore = 20
	lastTitle = ""
	for x in range(1, 21):
		quote1 = soupDiv.find("span", text=str(x)+".")
		quote2 = quote1.find_next_siblings('span')
		prevValue = next((item for item in titles if item["title"] == quote2[0].text), None)
		if prevValue == None:
			newTitle = {}
			newTitle['title'] = quote2[0].text
			newTitle['score'] = currentScore
			titles.append(newTitle)
		else:
			prevValue['score'] = prevValue['score'] + currentScore
		currentScore = currentScore - 1

def writeToFile(listToWrite):
	f = open('news','w')
	for item in listToWrite:
		f.write(item['title'] + " /Score: " + str(item['score']) + "\n")
	f.close()

def timerHandler():
	scanNews()
	sortedlist = sorted(titles, key=lambda k: k['score'])
	writeToFile(sortedList)
	threading.Timer(600, timerHandler).start()

timerHandler()
