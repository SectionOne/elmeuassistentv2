try:
    import pywhatkit as kit
except Exception as _e:
    # PyWhatKit realiza una comprobación de red al importarse y puede lanzar
    # una excepción si no hay conexión. Guardamos el error y continuamos para
    # que el módulo no falle al importarse.
    kit = None
    _pywhatkit_import_error = _e

import requests
import socket

def searchOnGoogle(query):
    if kit is None:
        raise RuntimeError(f"pywhatkit no disponible: {_pywhatkit_import_error}")
    kit.search(query)

def playOnYouTube(video_name):
    if kit is None:
        raise RuntimeError(f"pywhatkit no disponible: {_pywhatkit_import_error}")
    kit.playonyt(video_name)

def sendWhatsAppMessage(number, message):
    if kit is None:
        raise RuntimeError(f"pywhatkit no disponible: {_pywhatkit_import_error}")
    kit.sendwhatmsg_instantly(f"+34{number}", message)

def getRandomJoke():
    response = {"error": "", "joke": "", "answer": ""}

    # Primera comprobación rápida de conectividad (socket)
    try:
        # create_connection gestiona bien el timeout y cierra la conexión automáticamente
        with socket.create_connection(("www.google.com", 80), timeout=5):
            pass
    except (socket.gaierror, socket.timeout, OSError):
        response["error"] = "No hay conexión a Internet."
        return response

    # Intentar obtener el chiste desde la API y capturar cualquier error de requests
    try:
        headers = {'Accept': 'application/json'}
        res = requests.get("https://v2.jokeapi.dev/joke/Any?lang=es", headers=headers, timeout=7)
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.RequestException as e:
        response["error"] = f"Error al conectar al servicio de chistes: {e}"
        return response

    # Procesar la respuesta JSON
    if data.get('type') == 'single':
        response["joke"] = data.get('joke', '')
        response["answer"] = ""
    else:
        response["joke"] = data.get('setup', '')
        response["answer"] = data.get('delivery', '')

    return response

def getLlumOff():
    response = {}
    headers = { 'Accept': 'application/json'}
    response = requests.get("https://tuya.mipconline.es/index.php?status=off", headers=headers)
    return response

def getLlumOn():
    response = {}
    headers = { 'Accept': 'application/json'}
    response = requests.get("https://tuya.mipconline.es/index.php?status=on", headers=headers)
    return response