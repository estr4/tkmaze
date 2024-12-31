"""src/cell.py

Enthält Die Cell class, aus der das Labyrinth Besteht.
"""

class Cell:
    """
    Class, die eine Zelle darstellt.

    Attributes:
        pos_x (int): x-Position der Zelle im Labyrinth.
        pos_y (int): y-Position der Zelle im Labyrinth.
        visited (bool): markiert die Zelle as besucht oder unbesucht.
    """
    def __init__(self, pos_x , pos_y, visited = False):
        """
        __init__ wird aufgerufen, wenn eine Zelle Initialisiert wird.
        
        Args:
            pos_x (int): x-Position der Zelle im Labyrinth.
            pos_y (int): y-Position der Zelle im Labyrinth.
            visited (bool): markiert die Zelle as besucht oder unbesucht.
            walls (dict): Enthält die 4 Wände um die Zelle, diese können an oder aus sein.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.visited = visited
        self.walls = {
                "north": True,
                "south": True,
                "east": True,
                "west": True,
        }

    def is_wall_between(self, nb_cell) -> bool:
        """
        is_wall_between gibt True an, wenn die wand zu einem nachbar an oder aus ist.

        Args:
            nb_cell (Cell): die Nachbarzelle.

        Returns:
            bool: True, wenn es die Wand gibt, sonst False.
        """
        if self.pos_x == nb_cell.pos_x:   # Gleiche X
            if self.pos_y - nb_cell.pos_y == 1:  # Nachbar ist oben
                return self.walls["north"]
            if self.pos_y - nb_cell.pos_y == -1: # Nachbar ist unten
                return self.walls["south"]
        elif self.pos_y == nb_cell.pos_y: # Gleiche Y
            if self.pos_x - nb_cell.pos_x == 1:  # Nachbar ist links
                return self.walls["west"]
            if self.pos_x - nb_cell.pos_x == -1: # Nachbar ist rechts
                return self.walls["east"]

        return False

    def remove_wall_between(self, nb_cell):
        """
        remove_wall_between entfernt die wand zwischen 2 benachbarten Zellen.

        Args:
                nb_cell (Cell): die Nachbarzelle.
        """
        if self.pos_x == nb_cell.pos_x:  # Gleiche X
            if self.pos_y - nb_cell.pos_y == 1: # Nachbar ist oben
                self.walls["north"] = False
                nb_cell.walls["south"] = False
            if self.pos_y - nb_cell.pos_y == -1: # Nachbar ist unten
                self.walls["south"] = False
                nb_cell.walls["north"] = False
        elif self.pos_y == nb_cell.pos_y: # Gleiche Y
            if self.pos_x - nb_cell.pos_x == 1:  # Nachbar ist links
                self.walls["west"] = False
                nb_cell.walls["east"] = False
            if self.pos_x - nb_cell.pos_x == -1: # Nachbar ist rechts
                self.walls["east"] = False
                nb_cell.walls["west"] = False
