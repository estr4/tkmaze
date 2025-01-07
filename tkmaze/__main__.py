"""tkMaze: Eine 3d Labyrinth simulation in tkinter

für mehr Infos, beachte die Dokumentation im README.md.
Um das Program zu starten, führe dieses Modul mit python3 aus.
`python3 -m tkmaze`

.. Online Repository:
https://github.com/estr4/tkmaze
"""

import os
import tkinter as tk
from threading import Thread
from .cell import Cell
from .maze import Maze
from .render import Raycaster

def console(maze):
    """
    console erzeugt Python-Shell Output.

    Args:
        maze (Maze): Das Labyrinth.
    """
    print("Wilkommen zu tkMaze, einem 3d Labyrinth Generator!")
    while True:
        user = int(input("""
-----------------------------------------------------------------------------
                     |  Gebe an, was du machen möchtest!
                     |  [1] Gebe das Labyrinth as ASCII-Bild an
                     |  [2] Gebe das Labyrinth als liste an
                     |  [3] Beende das Program
                     ╰–> """))
        match user:
            case 1:
                print(maze)
            case 2:
                for row in list(maze):
                    print(row)
            case 3:
                os._exit(0) # schließt alle prozesse
            case _:
                print("Ungültige Eingabe!")

def window(maze):
    """
    window erzeugt tkinter Output.

    Args:
        maze (Maze): Das Labyrinth.
    """
    # initialisiert tkinter
    root = tk.Tk()
    root.title("tkmaze")

    # initialisiert den Raycaster
    r = Raycaster(maze, root)
    r.run()

if __name__ == "__main__":
    # dieser codeblock wird ausgefürt, wenn das programm gestartet wird
    m = Maze(5,6) # initialisiert ein labyrinth mit x * y zellen

    # generiert das Labyrinth (rekursiv oder iterativ)
    m.generate_dfs_iterative(m.grid[0][0])
    #m.generate_dfs_recursive(m.grid[0][0])


    # initialisiert 2 threads, damit die shell und das fenster voneinander unabhängig sind
    c = Thread(target=console, args=(m,))
    w = Thread(target=window, args=(m,))

    # startet die threads
    c.start()
    w.start()

    # wartet, bis die threads beendet werden, um das programm zu beenden
    c.join()
    w.join()
