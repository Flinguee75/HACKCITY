import subprocess
import sys
import os
import threading
import webbrowser
import time

def open_frontend():
    # Attendre que le serveur soit prêt
    time.sleep(2)
    webbrowser.open('http://localhost:3000')

def main():
    try:
        # Assurez-vous d'être dans le bon répertoire
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Utilisez le chemin Python actuel pour exécuter uvicorn
        subprocess.run([
            sys.executable, 
            "-m", 
            "uvicorn",
            "main:app",
            "--reload"
        ], check=True)
    except FileNotFoundError:
        print("Erreur: uvicorn n'est pas installé. Installez-le avec 'pip install uvicorn fastapi'")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du démarrage du serveur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 