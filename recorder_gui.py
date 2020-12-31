# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:19:02 2020

@author: Kevin Rozmiarek
"""

import serial as serial
import tkinter as tk
import datetime 

try:
    serialPort = 'COM6' #Will change based on port plugged into
    baudRate = 9600
    ser = serial.Serial(serialPort , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
    
except serial.SerialException:
    print('Port is open')    

def disconnect():
    ser.close()
    root.destroy()

def restartSerial():
    global ser
    log.insert(tk.END, 'Restarting comms')
    ser.close()
    serialPort = 'COM6' #Will change based on port plugged into
    baudRate = 9600
    ser = serial.Serial(serialPort, baudRate, timeout=0, writeTimeout=0) #ensure non-blocking

#make a TkInter Window
root = tk.Tk()
root.wm_title("Temperatue Recorder")

# make a scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

# make a text box to put the serial output
log = tk.Text(root, width=60, height=30, takefocus=0)
log.pack()

# attach text box to scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)

#Button to restart serial
restartButton = tk.Button(root, text="Restart Serial Comms", command = restartSerial)
restartButton.pack()

#Button to close correctly
closeButton = tk.Button(root, text="Exit", command = disconnect)
closeButton.pack()

#Temperature Displays
workingTemp1 = ""
workingTemp2 = ""
workingTemp3 = ""
workingTemp4 = ""

workingTemp1Display = tk.Label(root,text="Temp 1:"+str(workingTemp1), font=("Helvetica",16))
workingTemp1Display.pack(side = tk.LEFT)
workingTemp2Display = tk.Label(root,text="Temp 2:"+str(workingTemp2), font=("Helvetica",16))
workingTemp2Display.pack(side = tk.LEFT)
workingTemp3Display = tk.Label(root,text="Temp 3:"+str(workingTemp3), font=("Helvetica",16))
workingTemp3Display.pack(side = tk.LEFT)
workingTemp4Display = tk.Label(root,text="Temp 4:"+str(workingTemp4), font=("Helvetica",16))
workingTemp4Display.pack(side = tk.LEFT)


#make the buffers
serBuffer = ""
tempBuffer = ""
tempCounter = 1

def readSerial():
    while True:
        c = ser.read().decode("ascii") # attempt to read a character from Serial
        
        #was anything read?
        if len(c) == 0:
            break
        
        # get the buffers from outside of this function
        global serBuffer
        global tempBuffer
        global tempCounter
        
        # get the working temps from outside this function
        global workingTemp1
        global workingTemp2
        global workingTemp3
        global workingTemp4
        
        # check if character is a delimeter
        if c == '\r':
            c = '' # don't want returns. chuck it
            
        if c == '\n':
            #serBuffer += "\n" # add the newline to the buffer
            #add the line to the TOP of the log
            log.insert(tk.END, serBuffer)
            serBuffer = "" # empty the buffer
            
        if c == ',':
            
            if tempCounter == 1:
                workingTemp1 = tempBuffer
                tempCounter = 2
                tempBuffer = ""
                serBuffer += c
                
            elif tempCounter == 2:
                workingTemp2 = tempBuffer
                tempCounter = 3
                tempBuffer = ""
                serBuffer += c
                
            elif tempCounter == 3:
                workingTemp3 = tempBuffer
                tempCounter = 4
                tempBuffer = ""
                serBuffer += c
                
            elif tempCounter == 4:
                workingTemp4 = tempBuffer
                tempCounter = 1
                tempBuffer = ""
                serBuffer += c
            
        else:
            serBuffer += c # add to the serial buffer
            tempBuffer += c
    
    root.after(10, readSerial) # check serial again soon

def update_display():
    workingTemp1Display.config(text="Temp 1:"+str(workingTemp1))
    workingTemp2Display.config(text="Temp 2:"+str(workingTemp2))
    workingTemp3Display.config(text="Temp 3:"+str(workingTemp3))
    workingTemp4Display.config(text="Temp 4:"+str(workingTemp4))
    
    root.after(1,update_display)

# after initializing serial, an arduino may need a bit of time to reset
root.after(100, readSerial)
root.after(1,update_display)

root.mainloop()