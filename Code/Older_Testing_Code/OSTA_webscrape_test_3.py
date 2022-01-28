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
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

busNum = input("Please enter your bus number: ")

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
check_time = tableArea[17:endOfDate]

# Boolean Conditions
schoolsOpen = "schools are open" in tableArea
transportationNormal = "functioning normally" in tableArea

# Gets Redefined
result = requests.get("https://web.archive.org/web/20201125113958/http://www.ottawaschoolbus.ca/cancellation-delay-details/") ##### CHANGE LATER... FOR TESTING!
soup = bs4.BeautifulSoup(result.text,"lxml")
tableArea = soup.select("#bigTable")[0].getText()
busDelayed = busNum in tableArea

# School Status
if schoolsOpen:
    print("\t➼ Schools are open, unless otherwise stated in General Notices.")
else:
    print("\t➼ Schools are closed!")

# Transportation Status
if transportationNormal and not busDelayed:
    print("\t➼ All routes are functioning normally, unless otherwise stated in General Notices.")
elif busDelayed:
    result = [i for i in range(len(tableArea)) if tableArea.startswith(busNum, i)]
    
    #print (result) #### remove later
    
    print("\t➼ Your bus, " + str(busNum) + ", has been cancelled or delayed... The following are the official OSTA updates:")
    
    myobj = gTTS(text="Your bus, " + str(busNum) + ", has been cancelled or delayed as of " + check_time + "... The following are the official OSTA updates", lang="en", slow=False)
    myobj.save("TTS_message.mp3")
    os.system("mpg321 TTS_message.mp3")
    
    for i in range(0, len(result)):
        start = result[i]
        end = tableArea.find('\n', start)
        
        sub_str = tableArea[start:end]
        
        if "This" in sub_str:
            output_start = sub_str.find("This")
        else:
            output_start = sub_str.find("The")
        
        sub_str_2 = sub_str[output_start:]
        
        sub_str_3 = sub_str_2[:sub_str_2.find(".")]
        
        school = sub_str_2[sub_str_2.find(".") + 1:]
        
        print("\t\t➼ " + sub_str_3 + " for " + school)
        
        myobj = gTTS(text=sub_str_3 + " for " + school, lang="en", slow=False)
        myobj.save("TTS_message.mp3")
        os.system("mpg321 TTS_message.mp3")
        
else:
    print("\t➼ Bus routes have been cancelled. It's a snow day!")

# Final Outcome
if schoolsOpen and transportationNormal and not busDelayed:
    print("\nTherefore, transportation is functioning normally!")
    
    GPIO.output(18, True)
    time.sleep(3)
    GPIO.output(18, False)
    
    result = requests.get("http://www.ottawaschoolbus.ca/cancellation-delay-details/")
    soup = bs4.BeautifulSoup(result.text,"lxml")
    tableArea = soup.select("#tableArea")[0].getText()
    
    myobj = gTTS(text="As of " + tableArea[17:endOfDate] + ", schools are open and buses are functioning normally, unless otherwise stated in general notices. Hey Google, turn on the light and change it to green.", lang="en", slow=False)
    myobj.save("TTS_message.mp3")
    os.system("mpg321 TTS_message.mp3")
elif busDelayed:  #add timestamps
    print("\nTherefore, your bus has been delayed or cancelled!")
    
    GPIO.output(19, True)
    time.sleep(3)
    GPIO.output(19, False)
    
    if schoolsOpen:
        myobj = gTTS(text="OSTA states that schools are still open. Consider finding alternative transportation for today or attend classes remotely. Hey Google, turn on the light and change it to yellow.", lang="en", slow=False)
        myobj.save("TTS_message.mp3")
        os.system("mpg321 TTS_message.mp3")
        
else:
    print("\nTherefore, school's out for the day!")
    
    GPIO.output(20, True)
    time.sleep(3)
    GPIO.output(20, False)
    
    result = requests.get("http://www.ottawaschoolbus.ca/cancellation-delay-details/")
    soup = bs4.BeautifulSoup(result.text,"lxml")
    tableArea = soup.select("#tableArea")[0].getText()
    
    myobj = gTTS(text="As of " + tableArea[17:endOfDate] + ", schools are closed or buses have been cancelled. It is a snow day! Hey Google, turn on the light and change it to red.", lang="en", slow=False)
    myobj.save("TTS_message.mp3")
    os.system("mpg321 TTS_message.mp3")
