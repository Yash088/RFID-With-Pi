#!/usr/bin/env python
import RPi.GPIO as GPIO
import MFRC522
#import threading as
import signal
import MySQLdb
import threading as th
import time as tm
from datetime import time
from datetime import date
from datetime import datetime
global data
global result1
GPIO.setwarnings(False)
def end_read(signal,frame):
    print("Ctrl+C captured, ending read.")
    #continue_reading = False
    GPIO.cleanup()
    exit()

def get_the_uid():
    global uid
    global data
    global result1
    # If we have the UID, continue
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        # Check if authenticated
        data = str(uid[0])+" "+str(uid[1])+" "+str(uid[2])+" "+str(uid[3])
        #print(data)
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_StopCrypto1()
            #Select your datbase name and the column name
            query = ('SELECT name FROM ani.main WHERE uid_no = "' + str(data)+ '"')
            result1 = cur.execute(query)
            db.commit()
            
            
            
        else:
           print("Authentication error")
        
           
def printing_name(result1):
        global date1
        global result
        for row in cur.fetchall():
            name=str(row[0])
        
        if(result1==1):
             yo1="Welcome to the RAIOT Mr."+name
             print(yo1)
             date1=date.today()
             time1=datetime.time(datetime.now())
             query2 = ("SELECT* FROM ani.student WHERE date='"+str(date1)+"'AND uid='"+str(data)+"'")
             result=cur.execute(query2)
             db.commit()
        if(result == 0):
           inquery = ("INSERT INTO student(name,uid,date) VALUES('"+name+"','" + str(data) + "','"+str(date1)+"')")
           cur.execute(inquery)
           db.commit()
       #Updating Database
        elif(result1==1):
            query3 = ("UPDATE ani.student SET time_out='"+str(time1)+"' WHERE uid='"+str(data)+"' AND date='"+str(date1)+"'")
            cur.execute(query3)
            db.commit()

if __name__=="__main__":

    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    MIFAREReader = MFRC522.MFRC522()
    # Welcome messagedb
    print("Insert Your Card")
    while True:
        # Write your host name and user and passwd
        db = MySQLdb.connect(host="localhost", user="raiot" , passwd="raiotlab",db="ani")
        cur=db.cursor()
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card detected")
            
            first_thread=th.Thread( target=get_the_uid(), name="Uid")
            first_thread.start()
            
            if(result1==0):
                print("Authentication failed!!")
                continue
            first_thread.join()
            second_thread=th.Thread(target=printing_name(result1), name="Name")
            second_thread.start()
            tm.sleep(1)
            
        

