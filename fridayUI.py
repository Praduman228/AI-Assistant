import tkinter as tk
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import googletrans
import subprocess 
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def takevoicefortext():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening..")
        r.pause_threshold = 1.5
        audio = r.listen(source)
        try:
            print("Recognising")
            query2 = r.recognize_google(audio, language="en-in")
            query2 = query2.lower()
            print(f"User query: {query2}\n")
        except Exception as e:
            print(e)
            print("say again")
            return "None" 
        return query2

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Goodmorning")
        label2.config(text="Good Morning")
       
    elif hour >= 12 and hour < 18:
        speak("goodafter noon")
        label2.config(text="Good Afternoon")
       
    else:
        speak("goodevening")
        label2.config(text="Good Evening")

    speak("how may i help you")
    label2.config(text="how may i help you ?")
    


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening..")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Recognising.")
        query = r.recognize_google(audio, language="en-in")
        query = query.lower()
        print(f"User query: {query}\n")
       


    except Exception as e:
        print(e)

        print("Say that again")
        label2.config(text="Say That Again...")
        return "None"
    return query


def odbutton_click():

    speak("opening camera please wait..")
    
    label2.config(text="opening camera please wait..")
    vid=cv2.VideoCapture(0)
    while (True):
        ret,frame=vid.read()
        bbox,label,condfi=cv.detect_common_objects(frame)
        output=draw_bbox(img=frame,bbox=bbox,labels=label,confidence=condfi)
        cv2.imshow("Objectdetection",output)
        if cv2.waitKey(1) & 0xFF== ord("f"):
                break
    i=0
    sentance=[]
    for labels in label:
        if(i==0):
             sentance.append("I found a "+labels+" ")
        else:
            sentance.append(" and "+labels)
        i=i+1
    final="".join(sentance)
    label2.config(text=final)
    speak(final)
    


def button_click():
        query=takecommand()
        if "wikipedia" in query:
            speak("searching..Please wait")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            label2.config(text=result)
            speak(result)
        elif "open youtube" in query:
            webbrowser.open('https://www.youtube.com/')

        elif "search" in query:
            label2.config(text= "Opening Browser wait..")
            webbrowser.open(str(query))
        elif "detect" in query:
                speak("opening camera please wait..")
                label2.config(text="opening camera please wait..")
                vid=cv2.VideoCapture(0)
                while (True):
                    ret,frame=vid.read()
                    bbox,label,condfi=cv.detect_common_objects(frame)
                    output=draw_bbox(img=frame,bbox=bbox,labels=label,confidence=condfi)
                    cv2.imshow("Objectdetection",output)
                    if cv2.waitKey(1) & 0xFF== ord("f"):
                         break
                i=0
                sentance=[]
                for labels in label:
                    if(i==0):
                        sentance.append("I found a "+labels+" and ")
                    else:
                        sentance.append("a "+labels)
                    i=i+1
                final="".join(sentance)
                speak(final)
                label2.config(text=final)
        elif "voice to text" in query:
          
            speak('please tell me the content which you want to convert into text')
            label2.config(text="Please tell the content")
            text=takevoicefortext()
            speak("the converted text is")
            label2.config(text="Converting Speech to Text...")
            speak(text)
            label2.config(text=text)
        elif "good morning" in query:
            speak("good morning")
            label2.config(text="good morning")

        
        

if __name__== "__main__":
    
    root = tk.Tk()
    labeltext="FRIDAY AI ASSISTANT"
    # labeltext.configure(weight="bold")
    label = tk.Label(root, text=labeltext, font=("Arial", 18,"bold"), fg="#d19669",bg="lightblue",width=100)
    label.pack(padx=50,pady=50)
    root.configure(bg="lightblue") 
    root.title("Friday AI")
    root.geometry("800x600")
    button_font = ("Arial", 8, "bold")
    micbutton = tk.Button(root, text="MIC", command=button_click,width=10,height=3,bg="#d19669" ,fg="white",font=button_font)
    micbutton.pack(padx=30, pady=20) 
    odbutton = tk.Button(root, text="OBD", command=odbutton_click,width=10,height=3,bg="#d19669" ,fg="white",font=button_font)
    odbutton.pack(padx=20, pady=10) 
    label2 = tk.Label(root, text="", font=("Arial", 18), fg="#d19669",bg="lightblue",width=100,wraplength=500)
    label2.pack(padx=0,pady=50)
    wishme()
    root.mainloop()
   