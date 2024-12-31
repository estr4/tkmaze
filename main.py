"""tkMaze: Eine 3d Labyrinth simulation in tkinter

für mehr Infos, beachte die Dokumentation im README.md.
Um das Program zu starten, führe diese Datei mit python3 aus.

.. Online Repository:
https://github.com/estr4/tkmaze
"""

import os
import tkinter as tk
from threading import Thread
from src.cell import Cell
from src.maze import Maze
from src.render import Raycaster

def console(maze):
    """
    console erzeugt Python-Shell Output.

    Args:
        maze (Maze): Das Labyrinth.
    """
    print("Wilkommen zu tkMaze, einem 3d Labyrinth Generator!")
    while True:
        user = int(input("""
                     |  Gebe an, was du machen möchtest!
                     |  [1] Gebe das Labyrinth as ASCII-Bild an
                     |  [2] Gebe das Labyrinth als liste an
                     |  [3] Beende das Program
                     ╰-> """))
        match user:
            case 1:
                print(maze)
            case 2:
                for row in list(maze):
                    print(row)
            case 3:
                os._exit(0) # schließt alle prozesse

def window(maze):
    """
    window erzeugt tkinter Output.

    Args:
        maze (Maze): Das Labyrinth.
    """
    # initialisiere tkinter
    root = tk.Tk()
    root.title("tkmaze")

    # initialisiere den Raycaster
    r = Raycaster(maze, root)

if __name__ == "__main__":
    # dieser codeblock wird ausgefürt, wenn das programm gestartet wird
    m = Maze(5,6) # erstellt ein labyrinth mit x * y zellen

    # erstelle das Labyrinth (rekursiv oder iterativ)
    #m.generate_dfs_iterative(m.grid[0][0])
    m.generate_dfs_recursive(m.grid[0][0])


    # erstelt 2 threads, damit die shell und das fenster voneinander unabhängig sind
    c = Thread(target=console, args=(m,))
    w = Thread(target=window, args=(m,))

    # starte die threads
    c.start()
    w.start()

    # warte, bis die threads beendet werden, um das programm zu beenden
    c.join()
    w.join()
