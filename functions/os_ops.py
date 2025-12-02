import os
import subprocess as sp

paths = {
    "calculator": "C:\\Windows\\System32\\calc.exe"
}

def openCalculator():
    """Obre l'aplicació Calculadora de Windows."""
    calc_path = paths["calculator"]
    if os.path.exists(calc_path):
        sp.Popen(calc_path)
    else:
        print("No s'ha trobat la calculadora al camí especificat.")