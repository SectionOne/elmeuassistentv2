# Importar les llibreries necessàries
import json
import pyaudio
import vosk
import pyttsx3

# Inicialitzar el motor de síntesi de veu
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 120)  # Velocitat de la parla
engine.setProperty('voice', 'spanish')  # Idioma: espanyol
engine.say("Hola buenos dias. En que te puedo ayudar?")  # Missatge inicial
engine.runAndWait()  # Esperar a que acabi de parlar

def listen():
    """Funció per escoltar audio del micròfon i reconèixer la parla amb VOSK"""
    # Cargar el model de reconeixement de veu VOSK
    model = vosk.Model("model")
    rec = vosk.KaldiRecognizer(model, 16000)  # 16000 Hz de freqüència de mostreig
    
    # Inicialitzar el flux d'entrada d'audio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()
    
    print("Escoltant...")
    
    # Llegir dades d'audio continuadament fins detectar una frase completa
    while True:
        data = stream.read(4096, exception_on_overflow=False)  # Llegir fragment d'audio
        if rec.AcceptWaveform(data):  # ¿S'ha detectat una frase completa?
            result = rec.Result()  # Obtenir el resultat del reconeixement
            stream.stop_stream()  # Aturar el flux
            stream.close()  # Tancar el flux
            p.terminate()  # Finalitzar PyAudio
            return result  # Retornar el text reconegut

def listenToText():
    """Funció per convertir l'audio reconegut a text i extreure només el text"""
    c = listen()  # Escoltar i obtenir el resultat JSON de VOSK
    try:
        d = json.loads(c)  # Parsear el JSON
        return d.get('text', '')  # Extreure el camp 'text' del resultat
    except:
        return c  # Si hi ha error, retornar el resultat original


# Programa principal
print("Resultat:", listenToText())  # Escolta i mostra el text reconegut
print("Hola Clase que tal?")  # Missatge de despedida
