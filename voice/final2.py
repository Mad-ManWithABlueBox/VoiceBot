# rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
# rasa run actions
# run these two in separate terminals and then run final2.py

import speech_recognition as sr
import pyttsx3
import requests

engine = pyttsx3.init()

# Set the properties
engine.setProperty("rate", 150)  # Speech rate (words per minute)
engine.setProperty("volume", 0.8)  # Volume level (0.0 to 1.0)

bot_responses=[]

bot_message=""
message=""

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says : ",end=' ')
bot_responses.clear()
for i in r.json():
    bot_message = i['text']
    bot_responses.append(bot_message)
    print(f"{bot_message}")


# Convert text to speech
reply_text = " ".join(bot_responses)
engine.say(reply_text)

# Wait for speech synthesis to complete
engine.runAndWait() 


# while bot_message != "Bye" or bot_message!='thanks':
while bot_message != "Bye":

    # Create a recognizer object
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            message = r.recognize_google(audio)
            print("You said:", message)
        except sr.UnknownValueError:
            print("Unable to recognize speech")
        except sr.RequestError as e:
            print("Error: ", e)


    if len(message)==0:
        continue
    print("Sending message now...")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    print("Bot says : ",end=' ')
    bot_responses.clear()
    for i in r.json():
        bot_message = i['text']
        bot_responses.append(bot_message)
        print(f"{bot_message}")


    # Convert text to speech
    reply_text = " ".join(bot_responses)
    engine.say(reply_text)
    # Wait for speech synthesis to complete
    engine.runAndWait() 