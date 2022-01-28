# Import Statements
import requests
import bs4
#from replit import audio
import time
from gtts import gTTS
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

# Website to Scrape
result = requests.get("https://web.archive.org/web/20201125113958/http://www.ottawaschoolbus.ca/cancellation-delay-details/")

# Initializing the 'Soup' for Scraping
soup = bs4.BeautifulSoup(result.text,"lxml")

# Scraping the ID 'tableArea' that contains bus status data
tableArea = soup.select("#bigTable")[0].getText()
print(tableArea)

if "V97" in tableArea:
    print("Your bus has been cancelled or is delayed")
    
    #numOfRepeats = tableArea.count("V97")
    #print(str(numOfRepeats))
    
    result = [i for i in range(len(tableArea)) if tableArea.startswith("V97", i)]
    print(result)
    
    for i in range(0, len(result)):
        start = result[i]
        end = tableArea.find('\n', start)
        print(tableArea[start:end])
    
    #for i in range (0,numOfRepeats):
        #start = tableArea.find("V97") + 3
        #end = tableArea.find('\n', start)
        #print(tableArea[start:end])
