'''
The "AudiorecorderUI" program is a recording program designed with Tkinter. 
It accepts an MP3 stream and can record it for up to 200 seconds.

'''
__author__      = "Felix Hansmann"
__version__   = "3.10.6"

#import required packages
from tkinter import *
from tkinter import ttk
import threading
import re
import urllib.request
import os.path
import datetime

#Style of the UI is defined through constants
PADDING_X = 5
PADDING_Y = 5
FZ_HEADLINE = "30"
FZ_TEXT = "11"
TEXT_COLOR = "white"
ERR_TEXT_COLOR = "red"
BG_COLOR = "black"
MAIN_FONT = "Impact"
SECOND_FONT = "Arial"
BTN_BG_COLOR = "#0067B8"
BTN_BG_COLOR_EXECUTE = "green"
BTN_BG_COLOR_QUIT = "red"
BLOCKSIZE_OPTIONS = ["8", "16", "32", "64", "128", "256"]

#Initialization and declaration of Tkinter and the Style
root = Tk()
style = ttk.Style()
style.configure('TScale', background=BG_COLOR)

#Root Element
root.title("Audiorecorder")
root.minsize(500,500)
root.config(bg=BG_COLOR)

#Header Element
headerFrame = Frame(root)
headerFrame.pack()
headerFrame.config(bg=BG_COLOR)
LOGO = PhotoImage(file="assets/microphone.png")

#Input Elements
inputFrame = Frame(root)
inputFrame.pack()
inputFrame.config(bg=BG_COLOR)
URL_ICON = PhotoImage(file="assets/url.png")
FILE_ICON = PhotoImage(file="assets/file.png")
BLOCKSIZE_ICON = PhotoImage(file="assets/block.png")
DURATION_ICON = PhotoImage(file="assets/time.png")

#Information during recording
recordingDetails = Frame(root)
recordingDetails.pack()
recordingDetails.config(bg=BG_COLOR)

#Button Element (Execute und Quit)
btnFrame = Frame(root)
btnFrame.pack()
btnFrame.config(bg=BG_COLOR)

#Initialize the duration value to 0
current_value = 0

def getScaleValue():
    '''
    The function "getScaleValue" takes the duration value of a recording and returns it as a concatenated string.

    ''' 
    value = int(scaleDuration.get())
    return f"{value} Sekunden"

def sliderChanged(event):
    '''
    The function "sliderChanged" processes the text element with the value obtained from the "getScaleValue" function.

    Parameters
    ----------
    event : Object 
        scale change event
    ''' 
    selectedDuration.config(text=getScaleValue())

def errValidation(url, dataname, url_regex, dataname_regex):
    '''
    The function "errValidation" checks whether a URL, filename, and a syntactically correct URL/Dataname have been specified.

    Parameters
    ----------
    url : string
        URL of the mp3 stream
    dataname : strin
        Name of the saved file
    url_regex: string
        Regex Pattern of the Url
    dataname_regex: string
        Regex Pattern of the Dataname
    ''' 
    
    if not url_regex.match(url):
        valUrl.config(text="Bitte eine korrekte mp3-URL angeben.")
    else:
        valUrl.config(text="")
    if not dataname_regex.match(dataname):
        valDataname.config(text="Eingabe darf nicht leer sein und nur Buchstaben enthalten.")
    else:
        valDataname.config(text="")
   
def resetUrl(value):
    '''
    The function "resetUrl" clears the content of the URL input.    

    Parameters
    ----------
    value : String
        URL-Text
    ''' 
    textUrl.delete(0, "end")
    textUrl.insert(0, value)

def resetDatename(value):
    '''
    The function "resetDataname" clears the content of the dataname input.

    Parameters
    ----------
    value : String
        Dataname-Text
    ''' 
    textDataname.delete(0, "end")
    textDataname.insert(0, value)

def client_exit():
    '''
    The function "client_exit" exits the program.

    ''' 
    root.destroy()

'''Headline'''
#Logo Icon
logo = Label(headerFrame, image=LOGO, bg=BG_COLOR)
logo.grid(row=0, column=0, pady=PADDING_Y, sticky=E)
#Headline Text
headline = Label(headerFrame, fg=BTN_BG_COLOR, text="Audiorecorder", bg=BG_COLOR, font=f"{MAIN_FONT} {FZ_HEADLINE}",height=2)
headline.grid(row=0, column=1, pady=PADDING_Y)

'''URL Field'''
#URL Icon
urlIcon = Label(inputFrame, image=URL_ICON, bg=BG_COLOR)
urlIcon.grid(row=1, column=0, pady=PADDING_Y)
#URL Text
msgUrl = Label(inputFrame, text="MP3-Url:", bg=BG_COLOR, fg=TEXT_COLOR, font=f"{SECOND_FONT} {FZ_TEXT}")
msgUrl.grid(row=1, column=1, sticky=W, padx=PADDING_X, pady=PADDING_Y)
#URL Input
textUrl = Entry(inputFrame, width=30)
textUrl.grid(row=1, column=2, padx=PADDING_X, pady=PADDING_Y)
#URL Button (reset)
btnReset = Button(inputFrame, text=" X ",fg=TEXT_COLOR, bg=BTN_BG_COLOR, command = lambda: resetUrl(""), relief="flat")
btnReset.grid(row=1, column=3)

'''Dataname Field'''
#DatanameIcon
fileIcon = Label(inputFrame, image=FILE_ICON, bg=BG_COLOR)
fileIcon.grid(row=3, column=0, pady=PADDING_Y)
#DatanameI Text
msgDataname = Label(inputFrame, text="Name der Datei:", bg=BG_COLOR, fg=TEXT_COLOR, font=f"{SECOND_FONT}  {FZ_TEXT}")
msgDataname.grid(row=3, column=1, sticky=W, padx=PADDING_X, pady=PADDING_Y)
#DatanameI Input
textDataname = Entry(inputFrame, width=30)
textDataname.grid(row=3, column=2, padx=PADDING_X, pady=PADDING_Y)
#Dataname Button (reset)
btnReset = Button(inputFrame, text=" X ", fg=TEXT_COLOR, bg=BTN_BG_COLOR, command = lambda: resetDatename(""), relief="flat")
btnReset.grid(row=3, column=3)

'''Blocksize Field'''
#Blocksize Icon
blocksizeIcon = Label(inputFrame, image=BLOCKSIZE_ICON, bg=BG_COLOR)
blocksizeIcon.grid(row=5, column=0, pady=PADDING_Y)
#Blocksize Text
msgBlocksize = Label(inputFrame, text="Blocksize:", bg=BG_COLOR, fg=TEXT_COLOR, font=f"{SECOND_FONT} {FZ_TEXT}")
msgBlocksize.grid(row=5, column=1, sticky=W, padx=PADDING_X, pady=PADDING_Y)
#Blocksize Input
selectBlocksize = ttk.Combobox(inputFrame, values=BLOCKSIZE_OPTIONS, width=27)
selectBlocksize.set("8")
selectBlocksize.grid(row=5, column=2, sticky=W, padx=PADDING_X, pady=PADDING_Y)

'''Duration Field'''
#Duration Icon
durationIcon = Label(inputFrame, image=DURATION_ICON, bg=BG_COLOR)
durationIcon.grid(row=6, column=0, pady=PADDING_Y)
#Duration Icon
msgDuration = Label(inputFrame, text="Dauer der Aufnahme:", bg=BG_COLOR, fg=TEXT_COLOR, font=f"{SECOND_FONT} {FZ_TEXT}", height=4)
msgDuration.grid(row=6, column=1, sticky=W, padx=PADDING_X, pady=PADDING_Y)
#Duration Input
scaleDuration = ttk.Scale(inputFrame, from_=0, to= 200, length=185, orient=HORIZONTAL, command=sliderChanged, variable=current_value)
scaleDuration.grid(row=6, column=2, sticky=W, padx=PADDING_X, pady=PADDING_Y)
#Duration Output
selectedDuration = ttk.Label(inputFrame, text=getScaleValue(), background=BG_COLOR, foreground=TEXT_COLOR)
selectedDuration.grid(row=6,column=3,columnspan= 3)

'''Buttons (Execute and Quit)'''
#Execute Button
btnExecute = Button(btnFrame, text="Aufnehmen", width=15, height=1, fg=TEXT_COLOR, bg=BTN_BG_COLOR, font=f"{MAIN_FONT} {FZ_TEXT}",command = lambda: executeRecord(), relief="flat")
btnExecute.grid(row=0, column=1, padx=20, pady=10)
#Quit Button
btnQuit = Button(btnFrame, text="Beenden", width=15, height=1, fg=TEXT_COLOR, bg=BTN_BG_COLOR_QUIT, font=f"{MAIN_FONT} {FZ_TEXT}",command = lambda: client_exit(), relief="flat")
btnQuit.grid(row=0, column=2, padx=20, pady=10)

'''Recording Informations'''
recordInfo = Label(recordingDetails, text="", bg=BG_COLOR, font=f"{MAIN_FONT} {FZ_TEXT}")
recordInfo.grid(row=0, column=1, sticky=W)

'''Validation Messages'''
#URL Validation
valUrl = Label(inputFrame, text="", bg=BG_COLOR, fg=ERR_TEXT_COLOR)
valUrl.grid(row=2, column=1, columnspan=2, sticky=W, padx=PADDING_X)
#Dataname Validation
valDataname = Label(inputFrame, text="", bg=BG_COLOR, fg=ERR_TEXT_COLOR)
valDataname.grid(row=4, column=1, columnspan=2, sticky=W, padx=PADDING_X)

def recording():
    '''
    The "recording" function records an mp3 stream and saves it.

    ''' 
    try:
        #url_regex checks if the link starts with 'http/https' and ends with '.mp3'
        url_regex = re.compile(r'(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w.-]*)*/([\w-]+)\.mp3')
        #dataname_regex checks if the dataname has only letters 
        dataname_regex = re.compile(r'^[a-zA-Z]+$')
        
        url = textUrl.get()
        filename = textDataname.get()
        blocksize = selectBlocksize.get()
        duration = scaleDuration.get()
        
        #It is checked whether the URL and filename have been specified
        if filename and url and url_regex.match(url) and dataname_regex.match(filename):
            
            path = f"./{filename}.mp3"
            check_file = os.path.isfile(path)

            valUrl.config(text="")
            valDataname.config(text="")
            recordInfo.config(text="")
            
            #It is checked whether the file already exists
            if not check_file:
                btnExecute.config(text="Warte", state=DISABLED)
                recordInfo.config(text="Aufnahme läuft...", fg=TEXT_COLOR)
                stream = urllib.request.urlopen(url)
                start_time = datetime.datetime.now() 

                with open(f"{filename}.mp3", "wb") as f:
                    #It takes the provided URL and records according to the specified duration
                    while(datetime.datetime.now() - start_time).seconds < int(duration):
                        f.write(stream.read(int(blocksize)))

                    btnExecute.config(text="Aufnehmen", state=NORMAL)    
                    recordInfo.config(text="Aufnahme fertiggstellt.")
            else:
                valDataname.config(text="Dateiname bereits vergeben.")
        else:
            errValidation(url, filename, url_regex, dataname_regex)
    except Exception as error:
        #This is executed in case of unexpected errors
        btnExecute.config(text="Aufnehmen", state=NORMAL)
        recordInfo.config(text=f"URL wurde nicht gefunden.\nFehler: {error}", fg="red")

def executeRecord():
    '''
    The function "executeRecord" opens a new thread and executes the function "recording".

    ''' 
    threadRecord = threading.Thread(target=recording)
    threadRecord.start()
   
if __name__ == "__main__":
    root.mainloop()