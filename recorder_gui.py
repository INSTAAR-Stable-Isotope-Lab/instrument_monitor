# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:19:02 2020

@author: Kevin Rozmiarek
"""
# pyinstaller --icon=instaar_temp.ico -F --noconsole recorder_gui.py

import serial as serial
import tkinter as tk
import datetime
import os
import pathlib

#Serial start and com management 
###############################################################################

serialPort = 'COM11' #Will change based on port plugged into
baudRate = 9600

try:
    ser = serial.Serial(serialPort, baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
except serial.SerialException:
    print("Inital connection failed!")

def disconnect():
    ser.close()
    root.destroy()

def restartSerial(comPortName):
    global ser
    try:
        ser.close()
    except:
        print("Serial close unsuccessful")
    log.insert(tk.END, '\nRestarting comms at ' + str(comPortName))
    serialPort = comPortName #Will change based on port plugged into
    baudRate = 9600
    try:
        ser = serial.Serial(serialPort, baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
        
    except serial.SerialException:
        log.insert(tk.END, '\nThat did not work, you entered the COM port wrong!')
    root.after(10, readSerial)        

def restartCommsWindow():
    
   def restartCommsClose():
       restartCommsWindow.destroy()
       
   def buttonFunctions():
       global serialPort
       comPortName = str(comPortEntry.get())
       root.after(1, lambda: restartSerial(comPortName))
       restartCommsClose()
    
   restartCommsWindow = tk.Toplevel()
   restartCommsWindow.geometry('550x150')
   
   restartWindowLabel1 = tk.Label(restartCommsWindow, text= 'Please enter which COM port (Ex: COM1)',font=("Helvetica",16), height=2,width=34)
   restartWindowLabel1.pack()
   comPortEntry = tk.Entry(restartCommsWindow,font=("Helvetica",16))
   comPortEntry.pack()
   
   restartCommsWindowCloseButton = tk.Button(restartCommsWindow, text = 'Ok',height=1,font=("Helvetica",16),width = 25, command = buttonFunctions)
   restartCommsWindowCloseButton.pack()  

#Recording
###############################################################################

recording = False

def dataWindow():
    
   def dataWindowClose():
       dataWindow.destroy()
       
   def buttonFunctions():
       global recording
       recording=True
       recordSpeed = int(speedNumberEntry.get())
       fileName = str(runNumberEntry.get())
       root.after(1, lambda: recordData(recordSpeed, fileName))
       log.insert(tk.END, '\nStarting recording')
       dataWindowClose()
       
   dataWindow = tk.Toplevel()
   dataWindow.geometry('570x220')
   
   dataWindowLabel1 = tk.Label(dataWindow, text= 'Please enter file name:',font=("Helvetica",16), height=2,width=34)
   dataWindowLabel1.pack()
   runNumberEntry = tk.Entry(dataWindow,font=("Helvetica",16))
   runNumberEntry.pack()
   
   dataWindowLabel2 = tk.Label(dataWindow, text= 'How often do you want to record data? (1-??? seconds)',font=("Helvetica",16), height=2,width=44)
   dataWindowLabel2.pack()
   speedNumberEntry = tk.Entry(dataWindow,font=("Helvetica",16))
   speedNumberEntry.pack()
   
   dataWindowCloseButton = tk.Button(dataWindow, text = 'Ok',height=1,font=("Helvetica",16),width = 25, command = buttonFunctions)
   dataWindowCloseButton.pack()  

def recordData(recordSpeed, fileName):
    try:
        #os.chdir("/home/sil/Documents/Fixed_wing_ground_station_code/instaar/Boundary_Layer_Prediction/data")
        os.chdir(pathlib.Path(__file__).parent.absolute()/'data')
    except OSError:
        filler=1
        #log.insert(tk.END, '\nCannot find data folder, make one called "data"!')
    
    recordFileName=str(fileName)+".txt"
    recordFile  = open(recordFileName, "a")  
    currentDT = datetime.datetime.now()
    #decTime = (float(currentDT.minute)*60+float(currentDT.second))/3600
    recordFile.write(\
            str(currentDT)+','+\
            str(workingTemp1)+','+\
            str(workingTemp2)+','+\
            str(workingTemp3)+','+\
            str(workingTemp4)+'\n')  #Write string for data file!!!!!!
    recordFile.close()
    global recording
    if recording:
        root.after(recordSpeed*1000, lambda: recordData(recordSpeed, fileName))

def stopRecording():
    global recording
    recording = False
    log.insert(tk.END,'\nRecording ended')

#The GUI
###############################################################################

#make a TkInter Window
root = tk.Tk()
root.wm_title("Temperatue Recorder")

# make a scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

# make a text box to put the serial output
log = tk.Text(root, width=40, height=20, takefocus=0)
log.pack()

# attach text box to scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)

#Button to restart serial
restartButton = tk.Button(root, text="Restart Serial Comms", font=("Helvetica",14), command = restartCommsWindow)
restartButton.pack()

#Button to start recording
startRecordingButton = tk.Button(root, text="Start recording", font=("Helvetica",14),  command = dataWindow)
startRecordingButton.pack()

#Button to stop recording
stopRecordingButton = tk.Button(root, text="Stop recording", font=("Helvetica",14),  command = stopRecording)
stopRecordingButton.pack()

#Button to close correctly
closeButton = tk.Button(root, text="Exit", font=("Helvetica",14), command = disconnect)
closeButton.pack()

#Temperature display
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

#GUI Updating
###############################################################################

def update_display():
    workingTemp1Display.config(text="Temp 1:\n"+str(workingTemp1))
    workingTemp2Display.config(text="Temp 2:\n"+str(workingTemp2))
    workingTemp3Display.config(text="Temp 3:\n"+str(workingTemp3))
    workingTemp4Display.config(text="Temp 4:\n"+str(workingTemp4))
    
    root.after(1,update_display)

#Serial data handling
###############################################################################

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
            #log.insert(tk.END, serBuffer) If you want to insert the readlout to the log
            serBuffer = "" # empty the buffer
            tempBuffer = ""
            
        if c == ',':
            
            if tempCounter == 1:
                workingTemp1 = tempBuffer[1:]
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
    
###############################################################################

if __name__ == '__main__':
    root.after(100, readSerial)
    root.after(1,update_display)

    root.mainloop()