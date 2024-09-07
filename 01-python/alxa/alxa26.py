import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import pyautogui
from time import sleep
import webbrowser
import pywhatkit
from translate import Translator
import pyperclip
import datetime
import pyowm
arabe = {
    "أ": "h",
    "ب": "f",
    "ت": "j",
    "ث": "e",
    "ج": "[",
    "ح": "p",
    "خ": "o",
    "د": "]",
    "ذ": "`",
    "ر": "v",
    "ز": ".",
    "س": "s",
    "ش": "a",
    "ص": "w",
    "ض": "q",
    "ط": "'",
    "ظ": "/",
    "ع": "u",
    "غ": "y",
    "ف": "t",
    "ق": "r",
    "ك": ";",
    "ل": "g",
    "م": "l",
    "ن": "k",
    "ه": "i",
    "و": ",",
    "ي": "d",
    "ئ": "z",
    "ؤ": "c",
    "لا": "b",
    "ء": "x",
    "ة": "m",
    "ا": "h",
    " ":" "
}

phone_numbers={
"victor":"+201000723138",
"salma":"+201090518483",
"nada":"+201284724349"
}
lan = "en"
previous_lan = lan
#change_keyboard=0
no_change_keyboard_language=1



def voice(text):
    tts = gTTS(text=text, lang=lan, slow=False)
    audio_file = "output.mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)

def microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeout
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return None
    try:
        return recognizer.recognize_google(audio, language=lan)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as ex:
        print(f"An error occurred: {ex}")
    return None

def loop():
    text = None
    while text is None:
        text = microphone()
    return text

def translate_text(text, src_lang, dest_lang):
    trans = Translator(from_lang=src_lang, to_lang=dest_lang)
    translated_text = trans.translate(text)
    print(translated_text)  # Fixed the print statement
    return translated_text


def get_weather(city, api_key):
    # Initialize the OWM (OpenWeatherMap) object with the API key
    owm = pyowm.OWM(api_key)
    
    # Get the weather manager
    weather_mgr = owm.weather_manager()
    
    try:
        # Retrieve current weather for the city
        observation = weather_mgr.weather_at_place(city)
        weather = observation.weather
        
        # Extracting weather details
        temperature = weather.temperature('celsius')["temp"]
        humidity = weather.humidity
        status = weather.detailed_status
        
        # Print the weather data
        voice(f"{translate_text("Weather in","en",lan)} {translate_text(city,"en",lan)}:")
        voice(f"{translate_text("Temperature","en",lan)} {temperature}{translate_text("°C","en",lan)}")
        voice(f"{translate_text("Humidity","en",lan)} {humidity}%")
        voice(f"{translate_text("Description","en",lan)} {translate_text(status.capitalize(),"en",lan)}")
    
    except pyowm.commons.exceptions.NotFoundError:
        print("City not found, please check the city name.")
    except Exception as e:
        print(f"An error occurred: {e}")
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Arabic": "ar"
}

def choose_language():
    global lan, previous_lan,no_change_keyboard_language
    voice(translate_text("Choose a language", "en", lan))
    text = loop()
    if text:
        voice(translate_text("You said: ", "en", lan) + text)
        text = translate_text(text, lan, "en")
        previous_lan = lan
        for language, code in languages.items():
            if language.lower() in text.lower():
                lan = code
                print(lan)
                break
        if ((previous_lan == "ar" and lan != "ar") or (lan == "ar" and previous_lan != "ar")) and no_change_keyboard_language==1:
            no_change_keyboard_language=0

        
        #change_keyboard_language()
    else:
        voice("Sorry, I did not hear anything. Please try again.")
        choose_language()

def change_keyboard_language(text):
    global no_change_keyboard_language
    if ((previous_lan == "ar" and lan != "ar") or (lan == "ar" and previous_lan != "ar")) and no_change_keyboard_language==0:
        # Change keyboard layout to Arabic (Alt + Shift)
        sleep(0.1)
        pyautogui.keyDown('alt')
        sleep(0.1)
        pyautogui.press('shift')
        sleep(0.1)
        pyautogui.keyUp('alt')
        no_change_keyboard_language=1
    if lan=="ar":
        # Convert the Arabic text to corresponding key presses
        ls = []
        for i in text:
            if i in arabe:
                ls.append(arabe[i])

        # Join the key presses into a single string
        text_to_write = ''.join(ls)
        return text_to_write
    else:
        return text


def picture(x):
    try:
        image_path=None
        while image_path==None:
            pic=f"{x}.PNG"
            image_path =pyautogui.locateOnScreen(pic, confidence=0.8) 
            sleep(1)
        print(image_path)
        pyautogui.moveTo(image_path.left,image_path.top,duration=2)
        sleep(1)
        pyautogui.click(image_path.left,image_path.top)
        sleep(2)
    except pyautogui.ImageNotFoundException:
        print("image not found")


def word_search():
    try:
        image_path=None
        while image_path==None:
            image_path =pyautogui.locateOnScreen('search.PNG', confidence=0.8) 
            sleep(1)
        print(image_path)
        pyautogui.moveTo(image_path.left,image_path.top+10,duration=2)
        sleep(1)
        pyautogui.click(image_path.left,image_path.top+10)
        sleep(2)
    except pyautogui.ImageNotFoundException:
        print("image not found")


    

choose_language()
text = None

while True:
    text = loop()
    translated_text = translate_text(text, lan, "en")
    print(translated_text)
    if text:
        if "open" in   translated_text.lower():
            text1=translated_text.lower()
            text1=text1.split()
            print(translated_text)
            print(text1)
            if"opens" in text1:
                index=text1.index('opens')
                text1[index]="open"

            index=text1.index('open')
            index=index+1
            print(text1[index])
            if(text1[index].lower()=="chat"):
                webbrowser.open(f"https://www.chatgpt.com/")

            elif("youtube" in translated_text.lower()):
                if (lan=="ar"):
                    video=text.lower()
                    viedo=video.replace("افتح يوتيوب","",1).strip()
                    viedo=video.replace("ابحث عن","",1).strip()
                    pywhatkit.playonyt(video)

                elif  (lan=="fr"): 
                    video=text.lower()
                    viedo=video.replace("ouvre youtube","",1).strip()
                    viedo=video.replace("recherche","",1).strip() 
                    pywhatkit.playonyt(video)

                
                elif("search for" in translated_text.lower()):
                    video=translated_text.lower()
                    viedo=video.replace("open youtube","",1).strip()
                    viedo=video.replace("search for","",1).strip()
                    video=translate_text(video,"en",lan)
                    pywhatkit.playonyt(video)
                
                continue

            elif("google" in translated_text.lower()):
                if (lan=="ar"):
                    search=text.lower()
                    search=search.replace("افتح جوجل","",1).strip()
                    search=search.replace("ابحث عن","",1).strip()
                    pywhatkit.search(search)

                elif  (lan=="fr"): 
                    search=text.lower()
                    search=search.replace("ouvre google","",1).strip()
                    search=search.replace("recherche","",1).strip() 
                    pywhatkit.search(search)

             
                
                elif("search for" in translated_text.lower()):
                    search=text.lower()
                    search=search.replace("open google","",1).strip()
                    search=search.replace("search for","",1).strip()
                    #search=translate_text(search,"en",lan)
                    pywhatkit.search(search)
                
                continue
            elif("whatsapp" in translated_text.lower()):
                webbrowser.open(f"https://web.whatsapp.com/")
                sleep(20)
                picture("whatsapp")
                #whatsapp_search()
                a=translate_text("who you will text","en",lan)
                voice(a)
                person=loop()
                person=change_keyboard_language(person)
                pyautogui.write(person)
                sleep(1)
                pyautogui.press('enter')
                a=translate_text("what do you want to send","en",lan)
                voice(a)
                message=loop()
                message=change_keyboard_language(message)
                pyautogui.write(message)
                sleep(1)
                pyautogui.press('enter')
                 
            
            elif("word"in translated_text.lower()):
                pyautogui.hotkey('win')#will open the search
                pyautogui.typewrite('word')
                pyautogui.press('enter')
                sleep(2)
                pyautogui.press('enter')
            
            elif("facebook" in translated_text.lower()):
                pyautogui.hotkey('win')#will open the search
                pyautogui.typewrite('facebook')
                pyautogui.press('enter')

            elif "camera" in translated_text.lower():  
                pyautogui.hotkey('win')#will open the search
                pyautogui.typewrite('camera')
                pyautogui.press('enter')
                sleep(1)
                voice(translate_text("do you want to take a photo","en",lan))
                text=loop()
                text=translate_text(text,lan,"en")
                if "yes" in  text.lower():
                    picture("camera")

 
 

                
             
            else:
                webbrowser.open(f"https://www.{text1[index]}.com/")
            
        elif "language" in translated_text.lower():
            choose_language()

        elif "paste" in translated_text.lower():
            pyautogui.keyDown('ctrl')
            sleep(0.1)
            pyautogui.press('v')
            sleep(0.1)
            pyautogui.keyUp('ctrl')

        elif "tell" in translated_text.lower():
            if (lan=="ar"):
                    search=text.lower()
                    search=search.replace("اخبرني","",1).strip()
                    print(search)
                    search=change_keyboard_language(search)
                    webbrowser.open(f"https://www.chatgpt.com/")
                    sleep(1.5)
                    pyautogui.write(search, interval=0.1)
                    sleep(0.5)
                    pyautogui.press('enter')
                    sleep(25)
                    picture("copy")
                # Get text from the clipboard
                    copied_text = pyperclip.paste()
                    copied_text=copied_text.replace('"', '')
                    voice(copied_text)

            elif  (lan=="fr"): 
                search=text.lower()
                search=search.replace("dites-moi","",1).strip()
                webbrowser.open(f"https://www.chatgpt.com/")
                sleep(1.5)
                search=change_keyboard_language(search)
                pyautogui.write(search, interval=0.1)
                sleep(0.5)
                pyautogui.press('enter')
                sleep(25)
                picture("copy")
                # Get text from the clipboard
                copied_text = pyperclip.paste()
                copied_text=copied_text.replace('"', '')
                voice(copied_text)


            
            elif (lan=="en"):
                search=text.lower()
                search=search.replace("tell me ","",1).strip()
                webbrowser.open(f"https://www.chatgpt.com/")
                sleep(1.5)
                search=change_keyboard_language(search)
                pyautogui.write(search, interval=0.1)
                sleep(0.5)
                pyautogui.press('enter')
                sleep(20)
                #picture("sound")
                picture("copy")
                # Get text from the clipboard
                copied_text = pyperclip.paste()
                copied_text=copied_text.replace('"', '')
                voice(copied_text)

        elif "message" in translated_text.lower():
            if (lan=="en"):
                person=text.lower()
                person=person.replace("send message to ","",1).strip()
                voice("tell me what do you want to send")
                message=loop()
                pywhatkit.sendwhatmsg_instantly(phone_numbers[person], message)
            
            elif (lan=="ar"):
                person=translated_text.lower()
                person=person.replace("send a message to ","",1).strip()
                print(person)
                a=translate_text("tell me what do you want to send","en",lan)
                voice(a)
                message=loop()
                print(message)
                pywhatkit.sendwhatmsg_instantly(phone_numbers[person], message)
            elif (lan=="fr"):
                person=translated_text.lower()
                person=person.replace("send message to ","",1).strip()
                print(person)
                a=translate_text("tell me what do you want to send","en",lan)
                voice(a)
                message=loop()
                print(message)
                pywhatkit.sendwhatmsg_instantly(phone_numbers[person], message)


        elif "time" in translated_text.lower():
            now = datetime.datetime.now()
            a=translate_text("The current time is ","en",lan)
            voice(f"{a}{now.strftime('%H:%M:%S')}")
            #now.strftime('%H:%M:%S') formats the now object to display the current time in a 24-hour format: hours (%H), minutes (%M), and seconds (%S).

        elif "date" in translated_text.lower():
            now = datetime.datetime.now()
            a=translate_text("The current date is ","en",lan)
            voice(f"{a}{now.strftime('%Y-%m-%d')}")
            #now.strftime('%Y-%m-%d') formats the now object to display the current date in the format: year (%Y), month (%m), and day (%d).

        elif "weather" in translated_text.lower():
            # Replace 'your_api_key' with your actual API key
            api_key = "7f8a6c6355fa803c23ce4d67b15b305c"
            a=translate_text("tell me what is your city","en",lan)
            voice(a)
            city=loop()
            city=translate_text(city,lan,"en")
            get_weather(city, api_key)

        elif "write" in translated_text.lower():
            voice(translate_text("Tell me what do you want to write","en",lan))
            text=loop()
            text=change_keyboard_language(text)
            pyautogui.write(text, interval=0.25)
            pyautogui.write(" ")
             
        
        elif "search" in translated_text.lower():
                    webbrowser.open(f"https://www.chatgpt.com/")
                    voice(translate_text("what do you want to search","en",lan))
                    search=loop()
                    voice(translate_text("give me a 30 seconds to get the result of your search","en",lan))
                    search=change_keyboard_language(search)
                    sleep(0.5)
                    pyautogui.write(search, interval=0.1)
                    sleep(0.5)
                    pyautogui.press('enter');
                    sleep(30)
                    voice(translate_text("do you want to copy the result or search again or exit","en",lan))
                    text=loop()
                    translated_text=translate_text(text,lan,"en")
                    while "exit" not in translated_text:
                        if "copy" in translated_text:
                            picture("copy")
                            voice(translate_text("The result has been copied to the clipboard","en",lan))
                            voice(translate_text("do you want to search again or exit","en",lan))
                            text=loop()
                            translated_text=translate_text(text,lan,"en")
                            continue
                        elif "search" in translated_text:
                            picture("chat")
                            pyautogui.click()
                            voice(translate_text("what do you want to search","en",lan))
                            search=loop()
                            voice(translate_text("give me a 30 seconds to get the result of your search","en",lan))
                            search=change_keyboard_language(search)
                            sleep(1)
                            pyautogui.write(search, interval=0.25)
                            sleep(0.5)
                            pyautogui.press('enter')
                            sleep(30)
                            voice(translate_text("do you want to copy the result or search again or exit","en",lan))
                            text=loop()
                            translated_text=translate_text(text,lan,"en")
                        else:
                            continue
            
        elif "return" in translated_text.lower():
                picture("word")
        
        elif "scroll" in translated_text.lower():
           voice(translate_text("do you want to scroll up or down","en",lan)) 
           text=loop()
           if "up" in text:
                pyautogui.scroll(1000)  # scroll up by 100 units
           elif "down" in text:
                pyautogui.scroll(-1000)  # scroll down by 100 units
           while ("up" not in text) and ("down" not in text):
                text=loop()
                if "up" in text:
                        pyautogui.scroll(1000)  # scroll up by 100 units
                elif "down" in text:
                        pyautogui.scroll(-1000)  # scroll down by 100 units
               
        elif "like" in  translated_text.lower():
            picture("react")
        
        elif "comment" in translated_text.lower():
            picture("comment")
            voice(translate_text("what do you want to write in the comment","en",lan))
            text=loop()
            pyautogui.write(text, interval=0.25)
            sleep(0.5)
            pyautogui.press('enter')

        elif "meeting" in translated_text.lower():
            webbrowser.open(f"https://meet.google.com/landing")
            sleep(5)
            picture("meeting")
            picture("meeting1")
            sleep(20)
            picture("copy1")
        
        elif "translate" in translated_text.lower():
            trans=translated_text.lower()
            trans=trans.replace("translate to ","",1).strip()
            for language, code in languages.items():
                if language.lower() in trans.lower():
                    lan1 = code
                    print(lan1)
                    break
            x=pyperclip.paste()
            trans=translate_text(x,lan,lan1)
            print(trans)
            pyperclip.copy(trans)

            
            
     
    else:
        voice("Sorry, I did not hear anything. Please try again.")





        '''
        
        pywhatkit is a Python library that provides a simple interface for automating a variety of tasks, particularly those related to interacting with web services and media. It offers functionality for sending WhatsApp messages, playing YouTube videos, performing Google searches, and more.
        
        '''
