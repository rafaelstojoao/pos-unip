import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something")
    audio = r.listen(source)
    print("Ok thx")

try:
    print("Text: " + r.recognizer_google(audio));
except:
    pass;
