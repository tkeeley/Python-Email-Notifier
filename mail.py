
import imaplib, time, RPi.GPIO as GPIO

# Your email info
username = "your email address" #Type in your email address
password = "your password" #Type in your password


def init(): #Connects to your email, logs in and sets the GPIO. The print statements are for console use.
    print("[:\] Doing some nerdy connection things...") 
    mail = imaplib.IMAP4_SSL('imap-mail.outlook.com') #('imap.gmail.com') for gmail users
    mail.login(username, password) 
    print("[;)] Peeking into your inbox...") 
    print("[:)] Fiddling with your GPIO's...") 
    GPIO.setmode(GPIO.BCM) #Set up BCM GPIO numbering
    GPIO.setup(4, GPIO.OUT) #Sets GPIO 4 on your Pi as an output

    return mail

def newMail():
    GPIO.output(4, 1) #Sets GPIO 4 on your Raspi HIGH if there is an unread message.

def off(): #Sets GPIO 4 LOW. You have no new emails you sad lonely person.
    GPIO.output(4, 0)

def getMail(obj): 
    obj.select("inbox") 
    return len(obj.search(None, 'New')[1][0].split())

def checkMail(new): #Checks for new mail
    if checkMail != new: #Checks for change in the inbox so you don't keep triggering for the same new email
        if new >= 1: # If new mail is 1 or more it runs the newMail function
            print("[:)] New Mail! Way to go!!!") #Prints to the console you have a new email
            off() #Sets GPIO 4 LOW
            newMail() #Sets GPIO 4 HIGH
            time.sleep(5) #Keeps GPIO 4 HIGH for 5 Seconds
            off()#Turns GPIO 4 LOW

        else: #If new mail is 0 it leaves GPIO 4 LOW
            print("[:(] No new email. Sorry you have no friends") #Prints to console you have no new emails
            off() #Sets GPIO 4 LOW
    else:
        off()#Leaves GPIO 4 LOW if there is no change in the inbox 

def main(): #this is where the magic happens
    obj = init() 
    new = getMail(obj) 
    print(new) 
    checkMail(new)

    try: #Trys are a good thing. You should use them!
        while 1: #Do this stuff while true. a.k.a. until KeyboardInterrupt kills the program
            time.sleep(10) # Checks your email every 10 seconds
            new = getMail(obj)
            print(new) 
            checkMail(new) 
    except KeyboardInterrupt: #Get me outta here... (Ctrl + c)
        GPIO.cleanup() #Clean up the ports we've used resetting them back to input mode
        exit(0) #I'm out!

main() #Lets run this thing!


