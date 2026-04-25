"""UI helper class"""
import pygame
from ..Sprites import Image, Text, Button

class UI():
    """
    UI class for making the screen look nice and updating scores and fuel and such
    """    
    def __init__(self, screen: object, grav: float | int, sprite_group: pygame.sprite.LayeredUpdates):        
        self.screen       = screen 
        self.dim          = self.screen.get_size()
        self.gravity_mult = grav
        
        # Using the same sprite group taht is passed in from the main game
        self.sprites = sprite_group
        
        self.setup_layout()

    def setup_layout(self):
            """
            Sets up sprite layout and relative sizing
            """
            # -Layout Constants-
            self.padding =  self.dim[0] * 0.05
            self.panel_w = (self.dim[0] - (3 * self.padding)) // 2
            self.panel_h =  self.dim[1] * 0.85
            
            # -Dynamic offsets-
            margin_x   = self.dim[0] * 0.02   
            margin_y   = self.dim[1] * 0.02
            bar_height = self.dim[1] * 0.05   
            
            # -Font sizes-
            label_size = self.dim[0] // 27
            info_size  = self.dim[0] // 35
            
            # -Overlay-
            self.overlay = Image("Assets/Backgrounds/Panell.Png", (0,0), layer = 5, size = (self.dim[0], self.dim[1]))
            
            # -Panel Locators-
            left_x  = self.padding
            right_x = self.panel_w + (2 * self.padding)
            top_y   = (self.dim[1] - self.panel_h) // 2
            
            # Background dimensions 
            outlines      = ((160, 160, 160), (50, 50, 50))
            bg_color      = (104, 104, 104)
            label_bg_dim  = (self.panel_w * 0.27, label_size * 1.2)
            score_bg_dim  = (self.panel_w * 0.27, info_size * 1.1)
            
            # -Player 1 Elements-
            # Adding text and square behind text
            self.p1_label_bg = Button((left_x + margin_x*2.25, top_y + margin_y*1.7), label_bg_dim, bg_color, layer = 6, outline_col = outlines, radius = 10)
            self.p1_label    = Text("Player 1",    (left_x + margin_x*2.75, top_y + margin_y*2),              layer = 7, size = label_size)
            
            self.p1_score_bg = Button((left_x + self.panel_w - score_bg_dim[0] - margin_x*2.35, top_y + margin_y*2.25), score_bg_dim, bg_color, layer = 6, outline_col = outlines)
            self.p1_score    = Text("Score: 0000", (left_x + self.panel_w - margin_x*2.5, top_y + margin_y*2.45), layer = 7, size = info_size, anchor = "topright")
            
            # Fuel bar p1
            bar_dim          = (self.panel_w - (margin_x * 5), int(bar_height))
            self.p1_fuel_bar = Button((left_x + margin_x * 2.3, top_y + self.panel_h - bar_height * 1.6 - margin_y), bar_dim, (30, 30, 30), layer = 7, outline_col = outlines)
            
            # Coordinate tracker p1
            self.p1_coords = Text("X: 0000  Y: 0000", (left_x + margin_x * 8.5, top_y + margin_y * 6.6), layer=7, size=int(info_size//1.5))
            
            # -Player 2 Elements-
            # Adding text and square behind text
            self.p2_label_bg = Button((right_x + margin_x * 2.8, top_y + margin_y * 1.7), label_bg_dim, bg_color, layer = 6, outline_col = outlines)
            self.p2_label    = Text("Player 2",    (right_x + margin_x*3.3, top_y + margin_y*2),                layer = 7, size = label_size)
            
            self.p2_score_bg = Button((right_x + self.panel_w - score_bg_dim[0] - margin_x*2, top_y + margin_y*2.25), score_bg_dim, bg_color, layer = 6, outline_col = outlines)
            self.p2_score    = Text("Score: 0000", (right_x + self.panel_w - margin_x*2.15, top_y + margin_y*2.45), layer = 7, size = info_size, anchor = "topright")
            
            # Fuel bar p2
            self.p2_fuel_bar = Button((right_x + margin_x * 3.1, top_y + self.panel_h - bar_height * 1.6 - margin_y), bar_dim, (30, 30, 30), layer = 7, outline_col = outlines)
            
            # Coordinate tracker p2
            self.p2_coords = Text("X: 0000, Y: 0000", (right_x + margin_x  * 9, top_y + margin_y * 6.6), layer=7, size=int(info_size//1.5))
            
            # Adding everything to the group
            self.sprites.add(self.overlay, self.p1_label, self.p1_score, self.p1_fuel_bar, self.p1_label_bg, self.p1_score_bg, self.p2_label, self.p2_score, self.p2_fuel_bar, self.p2_label_bg, self.p2_score_bg, self.p1_coords, self.p2_coords)

    def update(self, players : pygame.sprite.Group):
        """
        Updating the fuel bars, score text and coordinates
        """
        p1, p2 = players
        
        # Update Fuel Bars
        self.p1_fuel_bar.resize(p1.fuel / 100)
        self.p2_fuel_bar.resize(p2.fuel / 100)
        
        # Update Score Text
        self.p1_score.update_text(f"Score: {p1.score:04d}", color = "red" if p1.score<0 else None)
        self.p2_score.update_text(f"Score: {p2.score:04d}", color = "red" if p2.score<0 else None)
        
        # Updating coordinates
        self.p1_coords.update_text(f"X: {int(p1.pos.x):04d}  Y: {int(p1.pos.y):04d}", color = "red" if 0 in p1.pos or 10000 in p1.pos else None)
        self.p2_coords.update_text(f"X: {int(p2.pos.x):04d}  Y: {int(p2.pos.y):04d}", color = "red" if 0 in p2.pos or 10000 in p1.pos else None)
        