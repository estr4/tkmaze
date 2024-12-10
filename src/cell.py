class Cell:
    """ Cell class:
        - representiert 1 Tile im Labyrinth
        - 4 Wände (Booleans für existiert und existiert nicht)
        - besucht (Boolean)
        - x and y Koordinaten
    """

    def __init__(self, pos_x: int, pos_y: int, visited: bool = False):
        "__init__ wird aufgerufen, wenn eine variable = Cell() gesetzt wird"
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.visited = visited
        self.walls = {
                "north": True,
                "south": True,
                "east": True,
                "west": True,
        }

    def is_wall_between(self, nb) -> bool:
        "gibt True an, wenn die wand zu einem nachbar existiert, sonst False"
        if self.walls["north"] and nb.walls["south"]:
            return True
        if self.walls["south"] and nb.walls["north"]:
            return True
        if self.walls["west"] and nb.walls["east"]:
            return True
        if self.walls["east"] and nb.walls["west"]:
            return True

        return False

    def remove_wall_between(self, nb):
        "entfernt die wand zwischen 2 nachbaren"
        if self.pos_x == nb.pos_x:  # Gleiches X
            if self.pos_y - nb.pos_y == 1:  # Nachbar ist oben
                self.walls["north"] = False
                nb.walls["south"] = False
            elif self.pos_y - nb.pos_y == -1:  # Nachbar ist unten
                self.walls["south"] = False
                nb.walls["north"] = False

        elif self.pos_y == nb.pos_y:  # Gleiche Y
            if self.pos_x - nb.pos_x == 1:  # Nachbar ist links
                self.walls["west"] = False
                nb.walls["east"] = False
            elif self.pos_x - nb.pos_x == -1:  # Nachbar ist rechts
                self.walls["east"] = False
                nb.walls["west"] = False
