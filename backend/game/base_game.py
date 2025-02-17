import pygame
import os
import win32gui  # Pour Windows
import win32con  # Pour Windows
import time

# Désactiver le message de bienvenue de Pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class BaseGame:
    def __init__(self, title):
        pygame.init()
        
        # Dimensions du jeu
        self.width = 800
        self.height = 600
        
        # Créer la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Masquer la console pour les jeux
        if os.name == 'nt':  # Windows
            try:
                console = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(console, win32con.SW_HIDE)
            except Exception as e:
                print(f"Erreur lors de la masquage de la console: {e}")
            
        # Attendre un peu que la fenêtre soit créée
        time.sleep(0.1)
        self.bring_to_front()
        
    def bring_to_front(self):
        try:
            # Trouver la fenêtre Pygame par son titre
            hwnd = win32gui.FindWindow(None, pygame.display.get_caption()[0])
            if hwnd:
                # Mettre au premier plan
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                # Essayer plusieurs fois de mettre au premier plan
                for _ in range(3):
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                        break
                    except:
                        time.sleep(0.1)
        except Exception as e:
            print(f"Erreur lors de la mise au premier plan: {e}") 