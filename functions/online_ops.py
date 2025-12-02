import pywhatkit as kit
import requests

def searchOnGoogle(query):
    kit.search(query)

def playOnYouTube(video_name):
    kit.playonyt(video_name)

def sendWhatsAppMessage(number, message):
    kit.sendwhatmsg_instantly(f"+34{number}", message)

def getRandomJoke():
    response = {}
    headers = {'Accept': 'application/json'}
    res = requests.get("https://v2.jokeapi.dev/joke/Any?lang=es", headers=headers).json()
    if res['type'] == 'single':
        response["joke"] = res['joke']
        response["answer"] = ""
    else:
        response["joke"] = res['setup']
        response["answer"] = res['delivery']
    return response