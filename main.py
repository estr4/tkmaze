"""
TkMaze: Eine 3d Labyrinth simulation in tkinter
Hilfreiche Links:
    -- Maze --
    https://en.wikipedia.org/wiki/Maze_generation_algorithm
    https://en.wikipedia.org/wiki/Maze-solving_algorithm
    https://en.wikipedia.org/wiki/Depth-first_search

    -- Raycasting --
    https://lodev.org/cgtutor/raycasting.html
"""
from src.cell import Cell
from src.maze import Maze
from src.render import Renderer

if __name__ == "__main__":
    # dieser codeblock wird ausgefürt, wenn das programm gestartet wird
    m = Maze(10,9)
    print(m)
