"""
Importiert Tkinter für Grafik
& math für mathematische funktionen
& time für sleep (abwarten)
"""
import tkinter as tk
#import math
#import time

class Renderer:
    """ Renderer class:
            - rendert das Labyrinth in 3D mithilfe von Raycasting und Tkinter
            - Raycasting ist ein weg, aus einer 2D "Karte" eine 3D welt zu erschaffen
    """

    def __init__(self, maze, width=800, height=600):
        "Initialisiert den Renderer mit dem Labyrinth und den Fenstergrößen."
        self.maze = maze # labyrinth, siehe maze.py
        self.width = width # breite in pixel
        self.height = height # höhe in pixel
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()
        self.player_pos = (self.width // 4, self.height // 2)  # Startposition des Spielers
        self.player_angle = 0  # Blickwinkel des Spielers in radianten

    def render(self):
        "Rendert das Labyrinth in 3D"
        pass

    def cast_rays(self):
        "Wirft Strahlen vom Spieler aus und prüft, ob sie auf Wände im Labyrinth treffen"
        pass

    def is_wall(self, x, y):
        "Prüft, ob der gegebene Punkt auf eine Wand im Labyrinth trifft."
        pass

    def draw_wall(self, ray, wall_height):
        "Zeichnet die Wand, die vom Strahl getroffen wird, auf den Bildschirm"
        pass
