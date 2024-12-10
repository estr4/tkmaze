"""
Importiert die Zellen, aus denen das Labyrinth besteht 
& random für zufällige generation
& sys für sehr tiefe rekursion
"""
import random
import sys
from .cell import Cell

sys.setrecursionlimit(100000)  # Sollte Sehr Hoch sein

#random.seed(1) # für debugging: macht random nicht mehr zufällig

class Maze:
    """ Maze class:
        - 2d Labyrinth aus Zellen
        - generiert mit folgendem algorithmus: https://en.wikipedia.org/wiki/Depth-first_search
        -> rekursiv
        - eingangspunkt = [0|0]
        - ausgangspunkt = [width|height]
    """

    def __init__(self, grid_width: int, grid_height: int):
        "__init__ wird aufgerufen, wenn eine variable = Maze() gesetzt wird"
        self.grid_width = grid_width
        self.grid_height = grid_height
        # generiert eine Array wie folgt: [[Cellx1y1, Cellx2y1,...], [Cellx1y2, Cellx2y2,...], ...]
        self.grid = [[Cell(x, y)
                      for y in range(grid_height)]
                      for x in range(grid_width)]

        # self.depth_first_iterative()
        self.depth_first_recursive(self.grid[0][0])

    def __iter__(self):
        "__iter__ erklärt python, wie man die Maze mit list() in eine array/liste umwandelt"
        for row in self.grid:
            yield from row

    def __str__(self) -> str:
        "__str__ erklärt python, wie man die Maze class in einen string umwandelt (z.B in print())"
        maze_str = ""
        for y in range(self.grid_height):
            # obere Wände für die Reihe
            top_line = ""
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
            mid_line += "|"  # Right boundary
            maze_str += top_line + "+\n" + mid_line + "\n"

        # untere Wand für die Letzte Reihe
        bottom_line = ""
        for x in range(self.grid_width):
            bottom_line += "+---"
        bottom_line += "+\n"
        maze_str += bottom_line

        return maze_str

    def get_neighbours(self, cell_index: tuple[int, int]):
        "gibt alle nachbaren einer Zelle wieder"
        x, y = cell_index
        neighbors = []
        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                neighbors.append(self.grid[nx][ny])
        return neighbors

    def get_unvisited_neighbours(self, cell_index: tuple[int, int]):
        "gibt alle unbesuchten nachbaren einer Zelle wieder"
        neighbors = self.get_neighbours(cell_index)
        return [nb for nb in neighbors if not nb.visited]

    def has_unvisited_neighbours(self, cell_index: tuple[int, int]) -> bool:
        "gibt an, ob noch unbesuchte nachbaren existieren"
        if self.get_unvisited_neighbours(cell_index):
            return True
        return False

    def depth_first_recursive(self, current_cell):
        "generiert ein (zufälliges) Labyrinth mit depth-fist-search"
        # Rekursive Version
        # "Base-Case" Szenario: Kein Nachbar ist unbesucht
        current_cell.visited = True
        current_index = (current_cell.pos_x, current_cell.pos_y)

        # Choose one of the unvisited neighbours
        unvisited_neighbors = self.get_unvisited_neighbours(current_index)
        random.shuffle(unvisited_neighbors)
        for neighbor in unvisited_neighbors:
            if not neighbor.visited:
                # Remove the wall between the current cell and the chosen cell
                current_cell.remove_wall_between(neighbor)
                # Invoke the routine recursively for the chosen cell
                self.depth_first_recursive(neighbor)

    def depth_first_iterative(self):
        "generiert ein (zufälliges) Labyrinth mit depth-first-search"
        # Iterative Version
        # Choose the initial cell, mark it as visited and push it to the stack
        stack = []
        start_cell = self.grid[0][0]
        start_cell.visited = True
        stack.append(start_cell)

        # While the stack is not empty
        while stack:
            # Pop a cell from the stack and make it a current cell
            current_cell = stack[-1]
            current_cell.visited = True
            current_index = (current_cell.pos_x, current_cell.pos_y)

            unvisited_neighbors = self.get_unvisited_neighbours(current_index)
            # If the current cell has any neighbours which have not been visited
            if unvisited_neighbors:
                # Choose one of the unvisited neighbours
                chosen_cell = random.choice(unvisited_neighbors)
                # Remove the wall between the current cell and chosen cell
                current_cell.remove_wall_between(chosen_cell)
                # Mark the chosen cell as visited and push it to the stack
                current_cell.visited = True
                stack.append(chosen_cell)
            else:
                # Backtrack
                stack.pop()
