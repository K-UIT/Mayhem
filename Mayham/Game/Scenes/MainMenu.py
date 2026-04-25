"""Main menu class"""
import pygame

from math      import sin
from ..Helpers import BaseScene
from ..Sprites import Stars, Image, Text, Button

class TitleScene(BaseScene):
    """
    Start menu with buttons leading to other screens
    """
    def __init__(self, screen : object, config : dict) -> None:
        """
        Setting up global time, making a sprite group and setting up initial layout
        """
        super().__init__(screen)
        
        # Setting up group
        self.sprites = pygame.sprite.LayeredUpdates()
        
        # Storing config dictionary
        self.config = config
        
        # Setting up time
        self.time = 0
        
        # Fix the layout to fit current screen
        self.setup_layout()
    
    def setup_layout(self) -> None:
        """
        Everything in here updates when the screen size changes
        """
        # Clear old sprites if the screen resized
        self.sprites.empty()
        
        # -Background-
        self.bg = Image(self.config["background"], (0,0), layer = 0, size = (self.screen_width, self.screen_height))
        
        # -Stars-
        self.stars = Stars((self.screen_width, self.screen_height*0.8), number = 100, layer = 1)
        
        # Button Dimensions
        btn_dim       = (self.screen_width // 4, self.screen_height // 6)
        btn_font_size = self.screen_width // 15

        # -Start button-
        start_pos         = (self.screen_width // 2 - btn_dim[0] // 2, self.screen_height // 2 - btn_dim[1] // 2)
        self.start_button = Button(start_pos, btn_dim, "green", layer = 2,  txt_size = btn_font_size, text = "START", outline_col = ("white", "darkgreen"))
        
        # -Settings button-
        sett_pos             = (self.screen_width // 2 - btn_dim[0] // 2, self.screen_height * 0.75 - btn_dim[1] // 2)
        self.settings_button = Button(sett_pos, btn_dim, "blue", layer = 2, txt_size = btn_font_size, text = "SETTINGS", outline_col = ("white", "darkblue"))
        
        # -Movable letters-
        title        = "MAYHEM"
        letter_space = self.screen_width // 16
        
        # Starting position for all the letters
        title_pos = ((self.screen_width // 2) - (letter_space * len(title) // 2), self.screen_width * 3 // 45)
        
        # List of all the letters
        self.letters = [Text(letter, (title_pos[0] + n*letter_space, title_pos[1]), 
                             layer = 3, size = self.screen_width // 8, color = "white") for n , letter in enumerate(title)]
        
        # Adding all sprites to the same group
        self.sprites.add(self.bg, self.stars, self.start_button, self.settings_button, self.letters)
        
    def handle_events(self, event : object) -> None|str:
        """
        Process input events and return the next scene
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
               if self.start_button.is_clicked(event.pos):      return "Game"
                   
               elif self.settings_button.is_clicked(event.pos): return "Settings"
                    
                    
    def update(self, dt : float) -> None:
        """
        Updating time, hovering over buttons, star flickering and movable letters
        """
        self.time += dt
        self.start_button.update()
        self.settings_button.update()
        
        self.stars.update(dt)
        
        # Updating the title
        for n, letter in enumerate(self.letters):
            # Having the letters move around in a wave pattern
            bob_factor = self.config["amplitude"] * sin(self.time * self.config["frequency"] + (n / 2))    
            
            letter.update_text(None, (letter.pos[0], letter.pos[1] + bob_factor))
        
    def draw(self) -> None:
        """Rendering all the sprites from the group"""
        self.sprites.draw(self.screen)