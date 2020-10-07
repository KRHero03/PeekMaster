
from tkinter import *
import tkinter.messagebox as messagebox
import shutil,os
import threading
import time
import pyaudio,wave
import pyautogui
from PIL import ImageGrab
import cv2
import numpy as np
import ffmpeg
# TKInter Variable 
RUNNING = True
STOPFLAG = 0

RECORDING_STATUS = 0
OUTPUT_PATH = os.path.expanduser("~/Desktop/")
TEMP_PATH = "/tmp/"
FILE_NAME = str(int(time.time()))

#Video Configuration

RESOLUTION = (pyautogui.size())
FPS = 40.00
CODEC = cv2.VideoWriter_fourcc(*"XVID")
videoOutput = None

# Audio Configuration

MICROPHONE = 1
MICROPHONE_DISABLED = 0
CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16
CHANNELS = 2
F = 38000
START_TIME = None
SILENCE =bytes(1)*4096

audioInstance = pyaudio.PyAudio()
stream = None
outputStream = None
audioFrames = []
outputFrames = []

outputDevice = audioInstance.get_default_output_device_info()["index"]
try:
    outputStream = audioInstance.open(format=SAMPLE_FORMAT,
                                channels=CHANNELS,
                                rate=F,
                                frames_per_buffer=CHUNK,
                                input=True,
                                input_device_index=outputDevice)   
except:
    pass

# Main Screen Configuration

root = Tk()
root.title("PeekMaster")
root.resizable(0,0)
root.option_add('*Dialog.msg.font', 'Roboto 10')


# Button Events

def startRecording():
    global RECORDING_STATUS,root,playButton,pauseIcon,playIcon
    global RESOLUTION,FPS,videoOutput,FILE_NAME,OUTPUT_PATH,CODEC
    global statusbar
    if RECORDING_STATUS == 0:
        response = messagebox.askyesno(title="PeekMaster - Start Recording", message="Are you sure you want to start Screen Recording?")
        if response==True:
            RECORDING_STATUS=1
            playButton.config(image=pauseIcon)
            root.wm_state('iconic')

            FILE_NAME = str(int(time.time()))
            videoOutput = cv2.VideoWriter(TEMP_PATH+FILE_NAME+'_video.avi',CODEC,FPS,RESOLUTION)
            RECORDING_STATUS = 1
            statusbar.config(text="Recording started")
        else:
            pass

    elif RECORDING_STATUS==1:   
        RECORDING_STATUS=2
        playButton.config(image=playIcon)
        statusbar.config(text="Recording paused")
    elif RECORDING_STATUS==2:
        RECORDING_STATUS=1
        playButton.config(image=pauseIcon)
        root.wm_state('iconic')
        statusbar.config(text="Recording continued")

def stopRecording():
    global RECORDING_STATUS,pauseIcon,playIcon,playButton,root
    if RECORDING_STATUS==2:        
        playButton.config(image=playIcon)
        RECORDING_STATUS = 3
        statusbar.config(text="Recording stopped")
    elif RECORDING_STATUS==0:
        messagebox.showinfo(title="PeekMaster - Message", message="PeekMaster is not Screen Recording!")
    elif RECORDING_STATUS==1:
        playButton.config(image=playIcon)
        RECORDING_STATUS=3
        statusbar.config(text="Recording stopped")

def toggleMicrophone():

    global microphoneButton,micOffIcon,MICROPHONE,micOnIcon,MICROPHONE_DISABLED
    if MICROPHONE_DISABLED==1:
        statusbar.config(text="Microphone disabled")
        detectMicrophone()
        if MICROPHONE_DISABLED==0:
            toggleMicrophone()
            statusbar.config(text="Microphone unmuted")
        return
    if MICROPHONE==1:
        MICROPHONE = 0
        microphoneButton.config(image=micOnIcon)
        statusbar.config(text="Microphone muted")
    else:
        MICROPHONE = 1
        microphoneButton.config(image=micOffIcon)
        statusbar.config(text="Microphone unmuted")

def detectMicrophone():
    global stream,MICROPHONE_DISABLED,SAMPLE_FORMAT,CHANNELS,F,CHUNK
    try:
        stream = audioInstance.open(format=SAMPLE_FORMAT,
                            channels=CHANNELS,
                            rate=F,
                            frames_per_buffer=CHUNK,
                            input=True)
        MICROPHONE_DISABLED = 0
    except:
        MICROPHONE_DISABLED = 1
        messagebox.showinfo(title="PeekMaster - Microphone not Detected",message="PeekMaster was unable to detect Microphone on your device.")


# def record(id):
#     global RECORDING_STATUS,MICROPHONE,OUTPUT_PATH,FILE_NAME
#     while(True):
#         print("RUNNING")


# Icons

playIcon = PhotoImage(file="./icons/play.png")
pauseIcon = PhotoImage(file="./icons/pause.png")
stopIcon = PhotoImage(file="./icons/stop.png")
micOnIcon = PhotoImage(file="./icons/micOn.png")
micOffIcon = PhotoImage(file="./icons/micOff.png")

# Buttons 

playButton = Button(root, image=playIcon,command=startRecording,relief=FLAT,bg="#fff")
microphoneButton = Button(root,image=micOffIcon,command=toggleMicrophone,relief=FLAT,bg="#fff")
stopButton = Button(root,image=stopIcon,command=stopRecording,relief=FLAT,bg="#fff" )



playButton.grid(row=0,column=1,padx=10,pady=10)
microphoneButton.grid(row=0,column=2,padx=10,pady=10)
stopButton.grid(row=0,column=3,padx=10,pady=10)

# Status Bar
statusbar = Label(root, text="Ready", bd=1, relief=FLAT, anchor=W)
statusbar.grid(row=1,column=1,columnspan=3)

# Centering Root Window

root.eval('tk::PlaceWindow . center')
root.eval(f'tk::PlaceWindow {str(root)} center')

# Show Instructions

messagebox.showinfo(title="PeekMaster - Instructions", message="PeekMaster is a Screen Recorder.\n\nHotkeys:-\nF1 - Start/Pause\nF2 - Mic On/Mic Off\nF3 - Stop\n\nMicrophone is set as ON by default.\nThe Output File is stored at the Desktop.")

# Root Key Bindings

root.bind_all("<F1>",startRecording)
root.bind_all("<F2>",toggleMicrophone)
root.bind_all("<F3>",stopRecording)

# Thread

# threading._start_new_thread(record,(1,))




# Runtime Procedueres


def toggleWindow():
    global RUNNING
    RUNNING = False
root.protocol("WM_DELETE_WINDOW", toggleWindow)

detectMicrophone()
if MICROPHONE_DISABLED==1:
    microphoneButton.config(image=micOnIcon)
    MICROPHONE = 0

# def record(id):
#     global STOPFLAG
#     global stream,audioFrames,outputStream,outputFrames
#     global RECORDING_STATUS
    
#     while STOPFLAG==0:
#         audioData = None
#         outputData = None
#     if stream is not None:
#         audioData = stream.read(CHUNK,exception_on_overflow = False)
#     if MICROPHONE==1 and RECORDING_STATUS==1 and audioData is not None:
#         audioFrames.append(audioData)
#     else:
#         audioFrames.append(SILENCE)
    
#     # if outputStream is not None:
#     #     outputData = outputStream.read(CHUNK,exception_on_overflow=False)
#     # if RECORDING_STATUS==1 and outputData is not None:
#     #     outputFrames.append(outputData)
#     # else:
#     #     outputFrames.append(SILENCE)

#     if RECORDING_STATUS==3:
        

#         # VOICE OUTPUT
#         wf = wave.open(OUTPUT_PATH+FILE_NAME+'_audio', 'wb')
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(audioInstance.get_sample_size(SAMPLE_FORMAT))
#         wf.setframerate(F)
#         wf.writeframes(b''.join(audioFrames))

#         audioFrames = []
#         outputFrames = []
#         # videoOutput = None
#         RECORDING_STATUS = 0
    
#     print("Audio Recording Thread Stopped")

# threading._start_new_thread(record,(id,))

while RUNNING==True:
    cv2.waitKey(25)
    root.update()
    audioData = None
    # outputData = None

    if stream is not None:
        audioData = stream.read(CHUNK,exception_on_overflow = False)
    if MICROPHONE==1 and RECORDING_STATUS==1 and audioData is not None:
        audioFrames.append(audioData)
    else:
        audioFrames.append(SILENCE)
    
    # if outputStream is not None:
    #     outputData = outputStream.read(CHUNK,exception_on_overflow=False)
    # if RECORDING_STATUS==1 and outputData is not None:
    #     outputFrames.append(outputData)
    # else:
    #     outputFrames.append(SILENCE)

    if RECORDING_STATUS==1:
        img = ImageGrab.grab()
        frame = np.array(img)

        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        videoOutput.write(frame)


    if RECORDING_STATUS==3:
        

        # VOICE OUTPUT
        wf = wave.open(TEMP_PATH+FILE_NAME+'_audio', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audioInstance.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(F)
        wf.writeframes(b''.join(audioFrames))

        # SPEAKER OUTPUT
        # wf = wave.open(OUTPUT_PATH+FILE_NAME+'_output', 'wb')
        # wf.setnchannels(CHANNELS)
        # wf.setsampwidth(audioInstance.get_sample_size(SAMPLE_FORMAT))
        # wf.setframerate(F)
        # wf.writeframes(b''.join(outputFrames))


        # VIDEO OUTPUT
        videoOutput.release()

        video = ffmpeg.input(TEMP_PATH+FILE_NAME+'_video.avi')
        audio = ffmpeg.input(TEMP_PATH+FILE_NAME+'_audio')
        out = ffmpeg.output(video, audio, OUTPUT_PATH+FILE_NAME+'.mp4', vcodec='copy', acodec='aac', strict='experimental')
        out.run()

        messagebox.showinfo(title="PeekMaster - Recording Complete", message="Your Screen Recording is complete!\nPlease find the file at your Desktop.")

        statusbar.config(text="Ready")

        audioFrames = []
        outputFrames = []
        videoOutput = None
        RECORDING_STATUS = 0

STOPFLAG = 1