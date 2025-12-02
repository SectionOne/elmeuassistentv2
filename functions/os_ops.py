import os
import subprocess as sp

paths = {
    "calculator": "C:\\Windows\\System32\\calc.exe",
    "discord": "C:\\Users\\Oriol\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    "vscode": "C:\\Users\\Oriol\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
}

def openCalculator():
    """Obre l'aplicació Calculadora de Windows."""
    calc_path = paths["calculator"]
    if os.path.exists(calc_path):
        sp.Popen(calc_path)
    else:
        print("No s'ha trobat la calculadora al camí especificat.")

def openDiscord():
    """Obre l'aplicació Discord."""
    discord_path = paths["discord"]
    if os.path.exists(discord_path):
        sp.Popen(discord_path)
    else:
        print("No s'ha trobat Discord al camí especificat.")

def openVSCode():
    """Obre l'aplicació Visual Studio Code."""
    vscode_path = paths["vscode"]
    if os.path.exists(vscode_path):
        sp.Popen(vscode_path)
    else:
        print("No s'ha trobat Visual Studio Code al camí especificat.")