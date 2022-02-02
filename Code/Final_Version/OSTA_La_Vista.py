'''
OSTA La Vista! -- A Webscraper Program

For Testing:
Snow Day/Buses Cancelled (Red Light): https://web.archive.org/web/20211206133450/http://www.ottawaschoolbus.ca/
V97 and Others Cancelled (Yellow Light): https://web.archive.org/web/20201125113958/http://www.ottawaschoolbus.ca/cancellation-delay-details/
All Transportation Operational (Green Light): https://web.archive.org/web/20201021102548/http://www.ottawaschoolbus.ca/cancellation-delay-details/
Current Transportation Status: http://www.ottawaschoolbus.ca/
'''

# Import Statements
import requests
import bs4
import time
from gtts import gTTS
import RPi.GPIO as GPIO
import os
import smtplib
import getpass
from tkinter import *
import datetime

# RPi GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

# Emailing Setup
smtp_object = smtplib.SMTP("smtp.gmail.com",587)
smtp_object.ehlo()
smtp_object.starttls()
from_address = "BafflingBusBot@gmail.com"
password = "tfajkbrbhweeurzo"    				# an 'App Password', that can only be used for emailing via a script!
smtp_object.login(from_address,password)
email_msg = []

# User Prompt
busNum = input("Please enter your bus number: ")
to_address = input("Please enter your email address: ")

# TTS Config
print("\nText to Speech Configuration:")
print("\t-> 'A' = ALWAYS enabled")
print("\t-> 'N' = NEVER enabled")
print("\t-> 'C' = CONDITIONALLY enabled; only enabled if buses are NOT cancelled (so that you can sleep in if they are!)")

wakeup_message = input("\nSelect an option above [A,N,C]: ").lower()

# If invalid input, alarm will be conditionally enabled
if wakeup_message != 'a' and wakeup_message != 'n' and wakeup_message != 'c':
    wakeup_message = 'c';

# GUI Alarm
def Alarm(set_alarm_timer):
    while True:
        time.sleep(1)
        actual_time = datetime.datetime.now()
        cur_time = actual_time.strftime("%H:%M:%S")
        cur_date = actual_time.strftime("%d/%m/%Y")
        msg="Current Time: "+str(cur_time) + ", Alarm Time: " + str(set_alarm_timer)
        print(msg)
        if cur_time == set_alarm_timer:
            print("Time to wake up!")
            window.destroy()
            break

# Gets User's Alarm Time
def get_alarm_time():
    alarm_set_time = hour.get() + ":" + min.get() + ":" + sec.get()
    Alarm(alarm_set_time)

# Tkinter GUI Window Config
window = Tk()
window.title("Alarm Clock")
window.geometry("400x160")
window.config(bg="#922B21")
window.resizable(width=True,height=True)
 
time_format=Label(window, text= "Remember to set time in 24 hour format!", fg="white",bg="#922B21",font=("Arial",15)).place(x=20,y=120)
addTime = Label(window,text = " Hour     Min      Sec  ",font=60,fg="white",bg="black").place(x = 210)
setYourAlarm = Label(window,text = "Set Time for Alarm: ",fg="white",bg="#922B21",relief = "solid",font=("Helevetica",13,"bold")).place(x=10, y=40)
 
hour = StringVar()
min = StringVar()
sec = StringVar()
 
hourTime= Entry(window,textvariable = hour,bg = "#48C9B0",width = 4,font=(20)).place(x=210,y=40)
minTime= Entry(window,textvariable = min,bg = "#48C9B0",width = 4,font=(20)).place(x=270,y=40)
secTime = Entry(window,textvariable = sec,bg = "#48C9B0",width = 4,font=(20)).place(x=330,y=40)
 
submit = Button(window,text = "Set Your Alarm",fg="Black",bg="#D4AC0D",width = 15,command = get_alarm_time,font=(20)).place(x =100,y=80)

# Continue Until Time is Set
window.mainloop()


# Website to Scrape
result = requests.get("http://www.ottawaschoolbus.ca/cancellation-delay-details/")      # current

# Initializing the 'Soup' for Scraping
soup = bs4.BeautifulSoup(result.text,"lxml")

# Scraping the ID 'tableArea' that contains bus status data
tableArea = soup.select("#tableArea")[0].getText()
#print(tableArea) --> Returns entire tableArea ID arrary (for testing)

# Pretty Formatting
endOfDate = tableArea.find("School Status")
print("\nAs of " + tableArea[17:endOfDate] + "...")
email_msg.append("As of " + tableArea[17:endOfDate] + "...")
check_time = tableArea[17:endOfDate]

# Boolean Condition
schoolsOpen = "schools are open" in tableArea

# 'result' Gets Redefined
#result = requests.get("https://web.archive.org/web/20211206133450/http://www.ottawaschoolbus.ca/")    # snow day
#result = requests.get("https://web.archive.org/web/20201021102548/http://www.ottawaschoolbus.ca/")    # normal
result = requests.get("http://www.ottawaschoolbus.ca/")    # current
soup = bs4.BeautifulSoup(result.text,"lxml")
tableArea = soup.select(".alert")[0].getText()

#print(tableArea) --> Returns entire alert class arrary (for testing)

# Boolean Condition
transportationNormal = not "cancelled" in tableArea

# 'result' Gets Redefined... again
#result = requests.get("https://web.archive.org/web/20201125113958/http://www.ottawaschoolbus.ca/cancellation-delay-details/")    # V97 cancelled
#result = requests.get("https://web.archive.org/web/20201021102548/http://www.ottawaschoolbus.ca/cancellation-delay-details/")    # normal
result = requests.get("http://www.ottawaschoolbus.ca/cancellation-delay-details/")    # current
soup = bs4.BeautifulSoup(result.text,"lxml")
tableArea = soup.select("#bigTable")[0].getText()
# Checking for their Bus Delay
busDelayed = busNum in tableArea

# School Status
if schoolsOpen:
    print("\t-> Schools are open, unless otherwise stated in General Notices.")
    email_msg.append("-> Schools are open, unless otherwise stated in General Notices.")
else:
    print("\t-> Schools are closed!")
    email_msg.append("-> Schools are closed!")

# Transportation Status
if transportationNormal and not busDelayed:
    print("\t-> All routes are functioning normally, unless otherwise stated in General Notices.")
    email_msg.append("-> All routes are functioning normally, unless otherwise stated in General Notices.")
    
    os.system("mpg321 temp_alarm_sound.mp3")
elif busDelayed:
    result = [i for i in range(len(tableArea)) if tableArea.startswith(busNum, i)]
        
    print("\t-> Your bus, " + str(busNum) + ", has been cancelled or delayed... The following are the official OSTA updates:")
    email_msg.append("-> Your bus, " + str(busNum) + ", has been cancelled or delayed... The following are the official OSTA updates:")
    
    if wakeup_message != 'n':
        myobj = gTTS(text="Your bus, " + str(busNum) + ", has been cancelled or delayed as of " + check_time + "... The following are the official OSTA updates", lang="en", slow=False)
        myobj.save("TTS_message.mp3")
        os.system("mpg321 TTS_message.mp3")
    
    for i in range(0, len(result)):
        # School Name Extraction from Cryptic String
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
        
        print("\t\t-> " + sub_str_3 + " for " + school)
        email_msg.append("-> " + sub_str_3 + " for " + school)
        
        if wakeup_message != 'n':
            myobj = gTTS(text=sub_str_3 + " for " + school, lang="en", slow=False)
            myobj.save("TTS_message.mp3")
            os.system("mpg321 TTS_message.mp3")        
else:
    print("\t-> Bus routes have been cancelled. It's a snow day!")
    email_msg.append("-> Bus routes have been cancelled. It's a snow day!")

# Final Outcome
if schoolsOpen and transportationNormal and not busDelayed:
    subject = "Transportation Normal With No Delays"
    print("\nTherefore, transportation is functioning normally!")
    email_msg.append("\nTherefore, transportation is functioning normally!")
    
    GPIO.output(18, True)
    time.sleep(3)
    GPIO.output(18, False)
    
    # To Fetch Time of Scrape
    result = requests.get("http://www.ottawaschoolbus.ca/cancellation-delay-details/")
    soup = bs4.BeautifulSoup(result.text,"lxml")
    tableArea = soup.select("#tableArea")[0].getText()
    
    if wakeup_message != 'n':
        myobj = gTTS(text="As of " + tableArea[17:endOfDate] + ", schools are open and buses are functioning normally, unless otherwise stated in general notices. Hey Google, turn on the light and change it to green.", lang="en", slow=False)
        myobj.save("TTS_message.mp3")
        os.system("mpg321 TTS_message.mp3")
elif busDelayed:
    subject = str(busNum) + " Has Been Delayed"
    print("\nTherefore, your bus has been delayed or cancelled!")
    email_msg.append("\nTherefore, your bus has been delayed or cancelled!")
    
    GPIO.output(19, True)
    time.sleep(3)
    GPIO.output(19, False)
    
    if schoolsOpen and wakeup_message != 'n':
        myobj = gTTS(text="OSTA states that schools are still open. Consider finding alternative transportation for today or attend classes remotely. Hey Google, turn on the light and change it to yellow.", lang="en", slow=False)
        myobj.save("TTS_message.mp3")
        os.system("mpg321 TTS_message.mp3")
        
        #email_msg.append("OSTA states that schools are still open. Consider finding alternative transportation for today or attend classes remotely.")
else:
    subject = "School's Out for Today"
    print("\nTherefore, school's out for the day!")
    email_msg.append("\nTherefore, school's out for the day!")
    
    GPIO.output(20, True)
    time.sleep(3)
    GPIO.output(20, False)
    
    # To Fetch Time of Scrape
    result = requests.get("http://www.ottawaschoolbus.ca/cancellation-delay-details/")
    soup = bs4.BeautifulSoup(result.text,"lxml")
    tableArea = soup.select("#tableArea")[0].getText()
    
    if wakeup_message == 'a':
        myobj = gTTS(text="As of " + tableArea[17:endOfDate] + ", schools are closed or buses have been cancelled. It is a snow day! Hey Google, turn on the light and change it to red.", lang="en", slow=False)
        myobj.save("TTS_message.mp3")
        os.system("mpg321 TTS_message.mp3")
    
# Finalizing the Email
end_of_msg = "\n".join(str(x) for x in email_msg)
final_msg = "Subject: " + subject + "\n" + "\n" + "BafflingBusBot here! The following updates have been issued:" + "\n\n" + end_of_msg + "\n" + "\n" + "Baffle On!" + "\n" + "- BafflingBusBot"
smtp_object.sendmail(from_address,to_address,final_msg)
smtp_object.quit()
