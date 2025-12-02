# Importar les llibreries necessàries
import json
import pyaudio
import vosk
import pyttsx3
import re
from datetime import datetime
from functions.os_ops import openCalculator, openDiscord, openVSCode
from functions.online_ops import searchOnGoogle, playOnYouTube, sendWhatsAppMessage

USERNAME = "Usuario"
BOTNAME = "laura"
# Usar un diccionario para mantener el estado de variables mutables
state = {
    'inactivity': 0,
    'greet': False,
    'dialog': False
}
inactivityMax = 2 # Nombre de cicles d'inactivitat abans de despedir-se

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
    hour = datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Buenos días {USERNAME}")
    elif 12 <= hour < 18:
        speak(f"Buenas tardes {USERNAME}")
    else:
        speak(f"Buenas noches {USERNAME}")
    speak(f"Soy {BOTNAME}, tu asistente virtual. ¿En qué puedo ayudarte hoy?")
    state['greet'] = True

def byeBye():
    """Funció per acomiadar-se de l'usuari"""
    hour = datetime.now().hour
    if hour >= 21 or hour < 6:
        speak(f"Buenas noches {USERNAME}, que descanses.")
    else:
        speak(f"Adiós {USERNAME}, hasta luego.")
    state['greet'] = False
    state['dialog'] = False

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
    stringInput = listenToText()  # Escoltar i obtenir el text reconegut
    if isContain(stringInput, ["hola " + BOTNAME, "ayudame " + BOTNAME, BOTNAME], debug=False):
        state['dialog'] = True  # Iniciar conversació

# Sequencia de sortida de la conversació
def outDialog():
    speak("Deseas que te ayude en algo más?")
    stringInput = listenToText()  # Escoltar el text reconegut
    if isContain(stringInput, ["si", "sí", "claro", "por favor"], debug=False):
        speak("¿En qué más puedo ayudarte?")
        state['dialog'] = True  # Mantenir la conversa
        state['inactivity'] = 0  # Reiniciar el comptador d'inactivitat
    else:
        speak(f"Encantada de haberte ayudado. Si necesitas algo más, solo tienes que llamarme {BOTNAME}.")
        byeBye()

def actions(stringInput):
    if isContain(stringInput, ["prueba", "test", "evaluación"], debug=False):
        speak("Esta es una prueba de funcionamiento.")
        outDialog()
    elif isContain(stringInput, ["abre la calculadora", "abre calculadora", "abre la calculadora por favor", "calculadora"], debug=False):
        speak("Abriendo la calculadora.")
        openCalculator()
    elif isContain(stringInput, ["abre discord", "abre el discord", "abre discord por favor", "discord"], debug=False):
        speak("Abriendo Discord.")
        openDiscord()
    elif isContain(stringInput, ["abre visual studio code", "abre vscode", "abre el code", "visual studio code", "vscode", "code", "visual studio"], debug=False):
        speak("Abriendo Visual Studio Code.")
        openVSCode()
    elif isContain(stringInput, ["busca en google", "busca en internet", "haz una búsqueda", "búscalo en google", "búscalo en internet", "google"], debug=False):
        speak("¿Qué quieres que busque en Google?")
        query = listenToText()
        if query:
            speak(f"Buscando {query} en Google.")
            searchOnGoogle(query)
        else:
            speak("No he entendido tu solicitud de búsqueda.")
    elif isContain(stringInput, ["reproduce en youtube", "pon un video en youtube", "busca un video en youtube", "youtube"], debug=False):
        speak("¿Qué video quieres que reproduzca en YouTube?")
        video_name = listenToText()
        if video_name:
            speak(f"Reproduciendo {video_name} en YouTube.")
            playOnYouTube(video_name)
        else:
            speak("No he entendido tu solicitud de video.")
    elif isContain(stringInput, ["envía un mensaje de whatsapp", "manda un whatsapp", "envía un whatsapp", "whatsapp"], debug=True):
        speak("¿A qué número quieres enviar el mensaje?")
        number = listenToText()
        speak("¿Cuál es el mensaje que quieres enviar?")
        message = listenToText()
        if number and message:
            speak(f"Enviando mensaje a {number} por WhatsApp.")
            sendWhatsAppMessage(number, message)
        else:
            speak("No he entendido el número o el mensaje.")
    else:
        speak("Lo siento, no he entendido tu solicitud.")

# Programa principal
# Afegim el try-except per capturar errors inesperats com que l'usuari faci Ctrl+C
try:
    while True:
        #Control de si s'ha iniciat conversació o no
        if state['dialog']:
            # Validació de la salutació
            if state['inactivity'] == 0 and not state['greet']: greet_user()  # Saludar l'usuari si no s'ha fet encara
            stringInput = listenToText()  # Escolta el text reconegut

            if isContain(stringInput, ["adiós","adiós " + BOTNAME, "hasta luego", "hasta luego " + BOTNAME, "gracias " + BOTNAME, "para " + BOTNAME], debug=False):
                byeBye()  # Acomiadar-se de l'usuari
                continue # Situarem el continue per tornar a la següent iteració del bucle principal
            else:
                # Procés de despedida per inactivitat
                if(state['inactivity'] < inactivityMax and stringInput == ""):
                    speak("¿En qué más puedo ayudarte?")
                    state['inactivity'] += 1  # Incrementar el comptador d'inactivitat
                elif stringInput != "":
                    print("En breve gestiono tu petición") # Missatge de processament
                    actions(stringInput)  # Realitzar accions segons el text reconegut
                    stringInput = ""  # Reiniciar l'entrada de text
                    state['inactivity'] = 0  # Reiniciar el comptador d'inactivitat
                else:
                    outDialog()  # Sortir de la conversa per inactivitat
                    state['inactivity'] = 0  # Reiniciar el comptador d'inactivitat
            print("Fi de cicle", state['inactivity'])  # Missatge de despedida
        else:
            print("In StandBy")
            inDialog()  # Esperar a que s'iniciï la conversa
except KeyboardInterrupt:
    byeBye()  # Acomiadar-se de l'usuari en cas d'interrupció