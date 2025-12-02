# Importar les llibreries necessàries
import json
import pyaudio
import vosk
import pyttsx3
import re

USERNAME = "Usuario"
BOTNAME = "laura"
inactivity = 0
greet = False
dialog = False

# Inicialitzar el motor de síntesi de veu
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 120)  # Velocitat de la parla
engine.setProperty('voice', 'spanish')  # Idioma: espanyol
engine.setProperty('volume', 1.0)  # Volum màxim

def speak(text):
    engine.say(text)  # Missatge personalitzat
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
        
def greet_user():
    """Funció per saludar l'usuari segons l'hora del dia"""
    from datetime import datetime
    hour = datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Buenos días {USERNAME}")
    elif 12 <= hour < 18:
        speak(f"Buenas tardes {USERNAME}")
    else:
        speak(f"Buenas noches {USERNAME}")
    speak(f"Soy {BOTNAME}, tu asistente virtual. ¿En qué puedo ayudarte hoy?")
    greet = True

def listenToText():
    """Funció per convertir l'audio reconegut a text i extreure només el text"""
    c = listen()  # Escoltar i obtenir el resultat JSON de VOSK
    try:
        d = json.loads(c)  # Parsear el JSON
        return d.get('text', '')  # Extreure el camp 'text' del resultat
    except:
        return c  # Si hi ha error, retornar el resultat original

# Funció per observar si un string es troba a una llista
def isContain(textInput, seeds, debug=False):
    """Comprovar si algun element de 'seeds' està contingut en 
    'textInput' i retorna True si troba alguna coincidència."""
    # Validació d'entrada
    if not textInput or not seeds:
        if debug:
            print(f"Debug isContain: textInput o seeds buits - textInput: '{textInput}', seeds: {seeds}")
            return False
    # Normalitzar el text d'entrada: minuscules, eliminar espais extra i netejar
    textInput_str = str(textInput).strip()
    # Normalitzar espais multiples a un sol espai
    textInput_normalized = re.sub(r'\s+', ' ', textInput_str)
    textInput_lower = textInput_normalized.lower()

    if debug:
        print(f"Debug isContain: textInput normalitzat - '{textInput_lower}'")
        print(f"Debug isContain: seeds - {seeds}")

    # Comprovar si algun element de seeds està contingut en textInput
    # Retorna True en la primera coincidència trobada
    for seed in seeds:
        if seed:
            seed_str = str(seed).strip().lower()
            
            # Trobar la seed en el text normalitzat
            found = seed_str in textInput_lower
            if debug:
                print(f"Debug isContain: Comprovant seed '{seed_str}' - Trobat: {found}")
            if found:
                return True
    
    if debug:
        print("Debug isContain: No s'ha trobat cap coincidència.")
    return False

# Sequencia d'entrada en conversació
def inDialog():
    global dialog
    stringInput = listenToText()  # Escoltar i obtenir el text reconegut
    if isContain(stringInput, ["hola " + BOTNAME, "ayudame " + BOTNAME, BOTNAME], debug=True):
        dialog = True  # Iniciar conversació

# Programa principal
while True:
    #Control de si s'ha iniciat conversació o no
    if dialog:
        # Validació de la salutació
        if inactivity == 0 and not greet: greet_user()  # Saludar l'usuari si no s'ha fet encara
        print(listenToText())  # Escolta i mostra el text reconegut
        print("Fi de cicle")  # Missatge de despedida
    else:
        print("In StandBy")
        inDialog()  # Esperar a que s'iniciï la conversa
