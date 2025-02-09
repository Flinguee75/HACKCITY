import subprocess
import sys
import threading
import webbrowser
import time

def open_frontend():
    # Attendre que le serveur soit prêt
    time.sleep(2)
    webbrowser.open('http://localhost:3000')

def main():
    try:
        # Lancer le frontend en arrière-plan
        frontend_thread = threading.Thread(target=open_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()

        # Lancer le serveur FastAPI
        subprocess.run(["uvicorn", "main:app", "--reload"], check=True)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main() 