"""src/render.py

Enthält die Raycaster Class für die Graphische darstellung des Labyrinthes
"""

import math
import tkinter as tk

class Raycaster:
    """
    Class, die einen Raycaster darstellt, welcher ein 2d Labyrinth ins 3-Dimensionale projeziert.

    Attributes:
        cell_data (Maze): Das Labyrinth bestehend aus Reihen von Zellen. 
        root (Tk): Das tkinter Fenster.
        map_data ([Maze]): Das Labyrinth als Liste bestehend aus Reihen von Zahlen.
        width (int): Länge des Fensters, am Anfang Länge des Monitors.
        height (int): Höhe des Fensters, am Anfang Höhe des Monitors.
        canvas (Canvas): Bereich des Fensters, in dem der Raycaster zeichnet.
        quit (bool): Signalisiert, ob das Fenster geschlossen wird.
        mov_speed (float): Geschwindigkeit des Spielers.
        rot_speed (float): Rotationsgeschwindigkeit des Spielers.
        pos ([float]): initiale x und y position des Spielers.
        dir ([float]): initiale x und y ausrichtung des Spielers
        plane ([float]): x und y ausrichtung der Kamera
        tgm (tuple(float, float)): cos und sin Werte einer Rotation.
        itgm (tuple(float, float)): Umgekehrte cos und sin Werte einer Rotation.
    """
    def __init__(self, cell_data, root):
        """
        __init__ wird aufgerufen, wenn ein Raycaster Initialisiert wird.

        Attributes:
            cell_data ([[Cell]]): das Labyrinth bestehend aus Reihen von Zellen. 
            root (Tk): das tkinter Fenster.
        """
        # Standardt Variablen
        self.cell_data = cell_data
        self.map_data = list(cell_data)
        self.root = root
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self._quit = False

        # Kamera Variablen
        self.mov_speed = 0.2
        self.rot_speed = 0.06
        self.pos = self.find_start()
        self.dir = [1.0, 0.0]
        self.plane = [0.0, 0.66]

        # Trigonometrie Variablen
        self.tgm = (math.cos(self.rot_speed), math.sin(self.rot_speed))
        self.itgm = (math.cos(-self.rot_speed), math.sin(-self.rot_speed))

    def run(self):
        """
        run startet den Raycaster.
        """
        self.root.protocol("WM_DELETE_WINDOW", self.destroy_window)

        self.root.bind('w', self.up_press)
        self.root.bind('a', self.left_press)
        self.root.bind('s', self.down_press)
        self.root.bind('d', self.right_press)

        while not self._quit:
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            self.canvas.delete('all')
            self.render()
            self.root.update()

    def destroy_window(self):
        """
        destroy_window setzt das quit signal zu True und zerstört das Fenster.
        """
        self._quit = True
        self.root.destroy()

    def render(self):
        """
        render führt den DDA-Algorithmus aus und zeichnet ein Bild auf den Canvas.
        """
        for x in range(self.width):
            # Kamera x-Position
            cam_x = 2 * x / self.width - 1
            # x und y Richtung des Strahls
            ray_dir = self.calculate_ray_direction(cam_x)
            # Position als Index in Map-data
            map_pos = [int(self.pos[0]), int(self.pos[1])]
            side_dist, delta_dist = self.calculate_delta_distances(ray_dir, map_pos)
            step = self.calculate_step(ray_dir)
            side, perp_wall_dist = self.perform_dda(map_pos, side_dist, delta_dist, step)
            line_height = int(self.height / perp_wall_dist) if perp_wall_dist != 0 else int('inf')
            self.draw_line(line_height, side, map_pos, x)

    def calculate_ray_direction(self, camera_x) -> list[float]:
        """
        calculate_ray_direction Berechnet die Richtung des Strahls basierend auf der Kameraposition.

        Args:
            camera_x (float): x-Koordinate in Kamera-Raum.

        Returns:
            [float]: x und y Richtung des Strahls.
        """
        ray_dir_x = self.dir[0] + self.plane[0] * camera_x
        ray_dir_y = self.dir[1] + self.plane[1] * camera_x
        return [ray_dir_x, ray_dir_y]

    def calculate_delta_distances(self, ray_dir, map_pos) -> tuple[list[float], list[float]]:
        """
        calculate_delta_distances Berechnet die Seiten- und Delta-Distanzen für den DDA-Algorithmus.

        Args:
            ray_dir ([float]): x und y Richtung des Strahls.
            map_pos ([int]): Position der Kamera als x und y Index in map_data.

        Returns:
            tuple([float], [float]): Seiten-Distanzen und Delta-Distanzen 
        """
        delta_dist_x = abs(1 / ray_dir[0]) if ray_dir[0] != 0 else float('inf')
        delta_dist_y = abs(1 / ray_dir[1]) if ray_dir[1] != 0 else float('inf')
        if ray_dir[0] < 0:
            side_dist_x = (self.pos[0] - map_pos[0]) * delta_dist_x
        else:
            side_dist_x = (map_pos[0] + 1.0 - self.pos[0]) * delta_dist_x
        if ray_dir[1] < 0:
            side_dist_y = (self.pos[1] - map_pos[1]) * delta_dist_y
        else:
            side_dist_y = (map_pos[1] + 1.0 - self.pos[1]) * delta_dist_y
        return [side_dist_x, side_dist_y], [delta_dist_x, delta_dist_y]

    def calculate_step(self, ray_dir) -> list[int]:
        """
        calculate_step Bestimmt die Schrittwerte für den DDA-Algorithmus.

        Args:
            ray_dir ([float]): x und y Richtung des Strahls.

        Returns:
            [int]: x und y Schrittwerte
        """
        # negativ, wenn x/y kleiner 0, sonst positiv
        step_x = -1 if ray_dir[0] < 0 else 1
        step_y = -1 if ray_dir[1] < 0 else 1
        return [step_x, step_y]

    def perform_dda(self, map_pos, side_dist, delta_dist, step) -> tuple[int, float]:
        """
        Führt den DDA-Algorithmus aus, um die Wand zu finden.

        Args:
            map_pos ([int]): Position der Kamera als x und y Index in map_data.
            side_dist ([float]): Länge des Strahls, um die 1. x/y Seite tu treffen.
            delta_dist ([float]): Länge des Strahls, um von einer x/y-Seite die nächste zu treffen.
            step (int): Inkrement-Wert um map_pos auf den Strahl zu Richten.

        Returns:
            tuple(int, float): die Getroffene Seite (x oder y zugewendet) und Distanz zu dieser.
        """
        hit = False
        side = 0
        # während noch keine Seite getroffen wurde
        while not hit: # Seite noch nicht getroffen, gehe zur nächsten Seite
            if side_dist[0] < side_dist[1]: # X-Seite, nicht getroffen
                side_dist[0] += delta_dist[0]
                map_pos[0] += step[0]
                side = 0
            else:                           # Y-Seite, nicht getroffen
                side_dist[1] += delta_dist[1]
                map_pos[1] += step[1]
                side = 1
            if self.map_data[map_pos[0]][map_pos[1]] > 0: # Seite getroffen
                hit = True
        if side == 0: # X-Seite
            perp_wall_dist = side_dist[0] - delta_dist[0]
        else:         # Y-Seite
            perp_wall_dist = side_dist[1] - delta_dist[1]
        return side, perp_wall_dist

    def draw_line(self, line_height, side, map_pos, x):
        """
        draw_line zeichnet eine vertikale Linie auf dem Canvas, um die Wand darzustellen.

        Args:
            line_height (int): Höhe der Wand.
            side (int): Gibt an, ob die zu zeichende Seite nach x oder y ausgerichtet ist.
            map_pos ([int]): Position der Wand als x und y Index in map_data.
            x (int): Pixelwert, auf welcher Länge die Linie gezeichnet werden soll.
        """
        draw_start = -line_height // 2 + self.height // 2
        draw_end = line_height // 2 + self.height // 2
        draw_start = max(draw_start, 0) # negative pixel existieren nicht
        draw_end = min(draw_end, self.height) # pixel über dem fenster existieren nicht

        # wählt Farbe je nach Zahl in map_data an der Position der Wand
        wallcolors = [[150,150,150], [50,50,50], [50,150,50], [0,0,150]]
        color = wallcolors[self.map_data[map_pos[0]][map_pos[1]]]

        if side:
            for k, v in enumerate(color):
                # verdunkelt pixel, je nach Seite
                color[k] = int(v / 1.2)

        # wandelt RGB Werte für tkinter in Hex um
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        # zeichet vertikale Linie auf Canvas
        self.canvas.create_line(x, draw_start, x, draw_end, fill=hex_color)

    def left_press(self, event):
        """
        left_press wird aufgerufen, wenn 'a' gedrückt wird, Spieler dreht sich nach links.

        Args:
            event (event): von tkinter genutzt, um einen Tastendruck mit der Funktion zu verbinden.
        """
        self.dir[1] = self.dir[0] * self.itgm[1] + self.dir[1] * self.itgm[0]
        self.dir[0] = self.dir[0] * self.itgm[0] - self.dir[1] * self.itgm[1]
        self.plane[1] = self.plane[0] * self.itgm[1] + self.plane[1] * self.itgm[0]
        self.plane[0] = self.plane[0] * self.itgm[0] - self.plane[1] * self.itgm[1]

    def right_press(self, event):
        """
        right_press wird aufgerufen, wenn 'd' gedrückt wird, Spieler dreht sich nach rechts.

        Args:
            event (event): von tkinter genutzt, um einen Tastendruck mit der Funktion zu verbinden.
        """
        self.dir[1] = self.dir[0] * self.tgm[1] + self.dir[1] * self.tgm[0]
        self.dir[0] = self.dir[0] * self.tgm[0] - self.dir[1] * self.tgm[1]
        self.plane[1] = self.plane[0] * self.tgm[1] + self.plane[1] * self.tgm[0]
        self.plane[0] = self.plane[0] * self.tgm[0] - self.plane[1] * self.tgm[1]

    def up_press(self, event):
        """
        up_press wird aufgerufen, wenn 's' gedrückt wird, Spieler läuft nach vorne.

        Args:
            event (event): von tkinter genutzt, um einen Tastendruck mit der Funktion zu verbinden.
        """
        if not self.map_data[int(self.pos[0] + self.dir[0] * self.mov_speed)][int(self.pos[1])]:
            self.pos[0] += self.dir[0] * self.mov_speed
        if not self.map_data[int(self.pos[0])][int(self.pos[1] + self.dir[1] * self.mov_speed)]:
            self.pos[1] += self.dir[1] * self.mov_speed

    def down_press(self, event):
        """
        down_press wird aufgerufen, wenn 's' gedrückt wird, Spieler läuft nach hinten.

        Args:
            event (event): von tkinter genutzt, um einen Tastendruck mit der Funktion zu verbinden.
        """
        if not self.map_data[int(self.pos[0] - self.dir[0] * self.mov_speed)][int(self.pos[1])]:
            self.pos[0] -= self.dir[0] * self.mov_speed
        if not self.map_data[int(self.pos[0])][int(self.pos[1] - self.dir[1] * self.mov_speed)]:
            self.pos[1] -= self.dir[1] * self.mov_speed

    def find_start(self) -> list[float]:
        """
        Findet den Start des Labyrinths, damit der Spieler nicht in eine Wand platziert wird.

        Returns:
                [float]: x und y Start-Werte
        """
        start_x = 2.5
        start_y = 1.5
        for x, row in enumerate(self.cell_data):
            for y, cell in enumerate(row):
                if cell == 2:
                    nb_cells = self.cell_data.get_connected_neighbors((x-1,y-1))
                    start_y = float(x / 2.0 + nb_cells[0].pos_x + 1.0) # wtf
                    start_x = float(y / 2.0 + nb_cells[0].pos_y + 1.0)
                    break

        start = [ start_x, start_y ]
        return start
