import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Habla algo...")
    audio = r.listen(source)

try:
    texto = r.recognize_google(audio, language="es-ES")
    print("Dijiste:", texto)
except:
    print("No entendí")