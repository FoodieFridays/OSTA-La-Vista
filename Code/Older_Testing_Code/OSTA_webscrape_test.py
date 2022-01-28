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
result = requests.get("http://www.ottawaschoolbus.ca/cancellation-delay-details/")

# Initializing the 'Soup' for Scraping
soup = bs4.BeautifulSoup(result.text,"lxml")

# Scraping the ID 'tableArea' that contains bus status data
tableArea = soup.select("#tableArea")[0].getText()
#print(tableArea)

# Formatting
endOfDate = tableArea.find("School Status")
print("As of " + tableArea[17:endOfDate] + "...")

# School Status
if "schools are open" in tableArea:
    print("\t➼ Schools are open, unless otherwise stated in General Notices.")
else:
    print("\t➼ Schools are closed!")

# Transportation Status
if "functioning normally" in tableArea:
    print("\t➼ All routes are functioning normally, unless otherwise stated in General Notices.")
else:
    print("\t➼ Bus routes have been cancelled. It's a snow day!")

# Final Outcome
if "schools are open" and "functioning normally" in tableArea:
    print("\nTherefore, transportation is functioning normally!")
    
    GPIO.output(18, True)
    time.sleep(3)
    GPIO.output(18, False)
    
    myobj = gTTS(text="As of " + tableArea[17:endOfDate] + ", schools are open and buses are functioning normally, unless otherwise stated in general notices. Hey Google, turn on the light and change it to green.", lang="en", slow=False)
    myobj.save("TTS_message.mp3")
    os.system("mpg321 TTS_message.mp3")
else:
    print("\nTherefore, school's out for the day!")
    
    GPIO.output(20, True)
    time.sleep(3)
    GPIO.output(20, False)
    
    myobj = gTTS(text="As of " + tableArea[17:endOfDate] + ", schools are closed or buses have been cancelled. It is a snow day! Hey Google, turn on the light and change it to red.", lang="en", slow=False)
    myobj.save("TTS_message.mp3")
    os.system("mpg321 TTS_message.mp3")