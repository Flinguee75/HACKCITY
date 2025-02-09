from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pygame
import json
import threading

# Import des jeux
from game.gorilla_game import GorillaGame
from game.horse_game import HorseGame
from game.whale_game import WhaleGame

app = FastAPI()

# Configurer CORS pour permettre la communication avec le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser Pygame
pygame.init()

class GameState:
    def __init__(self):
        self.running = False
        self.score = 0
        self.game_thread = None
        # Autres variables d'état du jeu

game_state = GameState()

def run_game(game_type: str):
    games = {
        "gorilla": GorillaGame,
        "horse": HorseGame,
        "whale": WhaleGame
    }
    
    game_class = games.get(game_type)
    if game_class:
        game = game_class()
        game.run()
    game_state.running = False

@app.post("/start-game/{game_type}")
async def start_game(game_type: str):
    print(f"Lancement du jeu: {game_type}")
    if game_state.running:
        print("Jeu déjà en cours")
        return {"status": "already_running"}
    
    try:
        if game_type not in ["gorilla", "horse", "whale"]:
            raise ValueError(f"Type de jeu inconnu: {game_type}")
            
        game_state.running = True
        print(f"Création du thread pour {game_type}")
        game_state.game_thread = threading.Thread(target=run_game, args=(game_type,))
        game_state.game_thread.start()
        print(f"Thread démarré pour {game_type}")
        return {"status": "started", "type": game_type}
    except Exception as e:
        print(f"Erreur lors du lancement: {str(e)}")
        game_state.running = False
        return {"status": "error", "message": str(e)}

@app.get("/game-state")
async def get_game_state():
    return {
        "score": game_state.score,
        "running": game_state.running
    }

@app.post("/update-mutation/{location}")
async def update_mutation(location: str):
    # Mettre à jour l'état du jeu en fonction de la localisation
    return {"status": "updated"}

# Ajouter cette route pour vérifier si le serveur est en marche
@app.get("/health-check")
async def health_check():
    return {"status": "ok"} 