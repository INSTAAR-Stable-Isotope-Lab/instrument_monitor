# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:19:02 2020

@author: Kevin Rozmiarek
"""

import serial as serial
import tkinter as tk
import datetime 


serialPort = "/dev/ttyACM0" #Will change based on port plugged into
baudRate = 9600
ser = serial.Serial(serialPort , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking

#make a TkInter Window
root = tk.Tk()
root.wm_title("Temperatue Recorder")

# make a scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack()#side = RIGHT, fill = Y)

# make a text box to put the serial output
log = tk.Text ( root, width=30, height=30, takefocus=0)
log.pack()

# attach text box to scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)

#make a buffer
serBuffer = ""

def readSerial():
    while True:
        c = ser.read() # attempt to read a character from Serial
        
        #was anything read?
        if len(c) == 0:
            break
        
        # get the buffer from outside of this function
        global serBuffer
        
        # check if character is a delimeter
        if c == '\r':
            c = '' # don't want returns. chuck it
            
        if c == '\n':
            serBuffer += "\n" # add the newline to the buffer
            
            #add the line to the TOP of the log
            log.insert('0.0', serBuffer)
            serBuffer = "" # empty the buffer
        else:
            serBuffer += c # add to the buffer
    
    root.after(10, readSerial) # check serial again soon


# after initializing serial, an arduino may need a bit of time to reset
root.after(100, readSerial)

root.mainloop()