import pywhatkit as kit

def searchOnGoogle(query):
    kit.search(query)

def playOnYouTube(video_name):
    kit.playonyt(video_name)

def sendWhatsAppMessage(number, message):
    kit.sendwhatmsg_instantly(f"+34{number}", message)