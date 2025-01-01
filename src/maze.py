"""src/maze.py

Enthält Die Maze class, die das Labyrinth darstellt.
"""

import random
import sys
from .cell import Cell

sys.setrecursionlimit(100000)  # Sollte Sehr Hoch sein
#random.seed(1) # für debugging: macht random nicht mehr zufällig

class Maze:
    """
    Class, die ein Labyrinth aus Zellen darstellt.

    Attributes:
        grid_width (int): länge des Labyrinths in Zellen.
        grid_height (int): höhe des Labyrinths in Zellen.
        grid ([[Cells]]): Labyrinth bestehend aus Reihen von Zellen.
    """
    def __init__(self, grid_width, grid_height):
        """
        __init__ wird aufgerufen, wenn ein Labyrinth Initialisiert wird.

        Args:
            grid_width (int): länge des Labyrinths in Zellen.
            grid_height (int): höhe des Labyrinths in Zellen.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        # generiert eine Array wie folgt: [[Cellx0y0, Cellx1y0,...], [Cellx0y1, Cellx1y1,...], ...]
        self.grid = [[Cell(x, y)
                      for y in range(grid_height)]
                      for x in range(grid_width)]

    def __iter__(self):
        """
        __iter__ wird aufgerufen, wenn man ein Objekt in eine Liste umwandelt.

        Yields:
            [int]: Labyrinth als Liste von Reihen mit Zahlen.
        """
        maze_iter = []
        for y in range(self.grid_height):
            # obere Wände
            top_line = []
            # Zellen-Reihe
            mid_line = []
            for x in range(self.grid_width):
                cell = self.grid[x][y]

                # Nördliche Wand
                top_line.append(1) # Ecken sind immer 1
                if cell.walls["north"]:
                    top_line.append(1)
                else:
                    top_line.append(0)

                # Linke Wand und Zelle selbst
                if cell.walls["west"]:
                    mid_line.append(1)
                else:
                    mid_line.append(0)
                mid_line.append(0)

            # Wand Ganz Rechts
            top_line.append(1)
            mid_line.append(1)
            maze_iter.append(top_line)
            maze_iter.append(mid_line)

        # untere Wand für die Letzte Reihe
        bottom_line = []
        bottom_line.extend([1] * (2 * self.grid_width + 1))
        maze_iter.append(bottom_line)

        # startzelle = 2 oben links, endzelle = 3 unten rechts
        maze_iter[1][1] = 2
        maze_iter[-2][-2] = 3

        yield from maze_iter

    def __str__(self) -> str:
        """
        __str__ wird aufgerufen, wenn man ein Object in ein String umwandelt.

        Returns:
            str: Labyrinth als ASCII-Bild.
        """
        maze_str = ""
        for y in range(self.grid_height):
            # obere Wände
            top_line = ""
            # Zellen-Reihe
            mid_line = ""
            for x in range(self.grid_width):
                cell = self.grid[x][y]

                # Nördliche Wand
                top_line += "+"  # Ecken sind +
                top_line += "---" if cell.walls["north"] else "   "

                # Linke Wand und Zelle selbst
                mid_line += "|" if cell.walls["west"] else " "
                mid_line += "   "

            # Wand Ganz Rechts
            mid_line += "|"
            maze_str += top_line + "+\n" + mid_line + "\n"

        # untere Wand für die Letzte Reihe
        bottom_line = ""
        for x in range(self.grid_width):
            bottom_line += "+---"
        bottom_line += "+\n"
        maze_str += bottom_line

        return maze_str

    def get_neighbors(self, cell_index) -> list[Cell]:
        """
        get_neighbors gibt alle Nachbaren einer Zelle wieder.

        Args:
            cell_index (tuple(int, int)): x und y koordinate einer Zelle im Labyrinth.

        Returns:
            [Cell]: alle Nachbaren einer Zelle.
        """
        x, y = cell_index
        nb_cells = []
        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy # Koordinaten der Nachbar-Zelle
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                nb_cells.append(self.grid[nx][ny])
        return nb_cells

    def get_unvisited_neighbors(self, cell_index) -> list[Cell]:
        """
        get_unvisited_neighbors gibt alle unbesuchten Nachbaren einer Zelle wieder.

        Args:
            cell_index (tuple(int, int)): x und y koordinate einer Zelle im Labyrinth.

        Returns:
            [Cell]: alle unbesuchten Nachbaren einer Zelle.
        """
        nb_cells = self.get_neighbors(cell_index)
        return [nb for nb in nb_cells if not nb.visited]

    def get_connected_neighbors(self, cell_index) -> list[Cell]:
        """
        get_connected_neighbors gibt alle verbundenen Nachbaren einer Zelle wieder.

        Args:
            cell_index (tuple(int, int)): x und y koordinate einer Zelle im Labyrinth.

        Returns:
            [Cell]: alle unbesuchten Nachbaren einer Zelle.
        """
        current_cell = self.grid[cell_index[0]][cell_index[1]]
        nb_cells = self.get_neighbors(cell_index)
        return [nb for nb in nb_cells if not current_cell.is_wall_between(nb)]

    def has_unvisited_neighbors(self, cell_index) -> bool:
        """
        has_unvisited_neighbors gibt an, ob es unbesuchte Nachbaren gibt.

        Args:
            cell_index (tuple(int, int)): x und y koordinate einer Zelle im Labyrinth.

        Returns:
            bool: True, wenn es unbesuchte Nachbaren gibt, sonst False
        """
        if self.get_unvisited_neighbors(cell_index):
            return True
        return False

    def generate_dfs_recursive(self, current_cell):
        """
        generate_dfs_recursive generiert ein (zufälliges) Labyrinth mit depth-fist-search rekursiv.

        Args:
            current_cell (Cell): Die momentan besuchte Zelle.
        """
        # Rekursive Version
        # "Base-Case" Szenario: alle Zellen sind besucht
        current_cell.visited = True
        current_index = (current_cell.pos_x, current_cell.pos_y)

        # Choose one of the unvisited neighbors
        unvisited_nb_cells = self.get_unvisited_neighbors(current_index)
        random.shuffle(unvisited_nb_cells)
        for nb in unvisited_nb_cells:
            if not nb.visited:
                # Remove the wall between the current cell and the chosen cell
                current_cell.remove_wall_between(nb)
                # Invoke the routine recursively for the chosen cell
                self.generate_dfs_recursive(nb)

    def generate_dfs_iterative(self, start_cell):
        """
        generate_dfs_iterative generiert ein (zufälliges) Labyrinth mit depth-fist-search iterativ.

        Args:
            start_cell (Cell): Die als erstes zu besuchende Zelle.
        """
        # Iterative Version
        # Choose the initial cell, mark it as visited and push it to the stack
        stack = []
        start_cell.visited = True
        stack.append(start_cell)

        # While the stack is not empty
        while stack:
            # Pop a cell from the stack and make it a current cell
            current_cell = stack[-1]
            current_cell.visited = True
            current_index = (current_cell.pos_x, current_cell.pos_y)

            unvisited_nb_cells = self.get_unvisited_neighbors(current_index)
            # If the current cell has any neighbors which have not been visited
            if unvisited_nb_cells:
                # Choose one of the unvisited neighbors
                chosen_cell = random.choice(unvisited_nb_cells)
                # Remove the wall between the current cell and chosen cell
                current_cell.remove_wall_between(chosen_cell)
                # Mark the chosen cell as visited and push it to the stack
                current_cell.visited = True
                stack.append(chosen_cell)
            else:
                # Backtrack
                stack.pop()
