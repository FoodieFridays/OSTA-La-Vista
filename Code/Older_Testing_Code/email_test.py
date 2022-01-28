import smtplib
import getpass

smtp_object = smtplib.SMTP("smtp.gmail.com",587)
smtp_object.ehlo()
smtp_object.starttls()

email = input("Please enter your email: ")
password = getpass.getpass("Please enter your *APP* password: ")
smtp_object.login(email,password)

#from_address = email
from_address = email
to_address = input("Please enter the email of the recipient: ")
subject = input("Enter what you want the subject line to be: ")
message = input("Enter what you want your message to be: ")
#message = ["\thello","\tjoe","\tmoe","grow"]
final_msg = "Subject: " + subject + "\n" + message
final_msg = "Subject: " + subject + "\n" + "\n".join(str(x) for x in message)


smtp_object.sendmail(from_address,to_address,final_msg)

smtp_object.quit()