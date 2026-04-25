"""Global game loop"""
import pygame, sys

# Different screens
from .Scenes import Mayhem, TitleScene, Settings

# Configs
from Config import Configure

class Gameloop():
    """
    Main game loop, draws everything and chooses screen size
    """
    def __init__(self):
        pygame.init()
        
        # Defining configs
        self.config = Configure
        
        # Setting up the screen
        self.screen_width  = self.config["screen_width"]
        self.screen_height = self.config["screen_height"]
        
        # Full screen logic
        flags = pygame.SCALED
        if self.config.get("full_screen"): flags |= pygame.FULLSCREEN
            
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags)
        
        # Naming window
        self.title = f"Mayhem ({self.config['start']})"
        pygame.display.set_caption(self.title)
        
        # Running logic
        self.fps     = self.config["fps"]
        self.clock   = pygame.time.Clock()
        self.running = True
        
        # Scene initialization
        if    self.config["start"] == "Game":     self.current_scene = Mayhem(    self.screen, self.config)
        elif  self.config["start"] == "Settings": self.current_scene = Settings(  self.screen, self.config)
        else: self.current_scene                                     = TitleScene(self.screen, self.config)
    
    def _apply_display_settings(self) -> None:
        """
        Safely rescaling the display 
        """        
        # Updating screen size 
        self.screen_width, self.screen_height = self.config["screen_width"], self.config["screen_height"]
        
        # Full screen flagging
        flags = pygame.SCALED
        if self.config["full_screen"]: flags |= pygame.FULLSCREEN
            
        # Recreate the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags)
        pygame.display.set_caption(self.title)
        
        # Update current scene references
        self.current_scene.screen = self.screen
        self.current_scene.screen_width = self.screen_width
        self.current_scene.screen_height = self.screen_height
        
        # Set up scene with new  layout
        self.current_scene.setup_layout()

    def _event_handler(self) -> None:
            """
            Checks for scene changes and triggers
            """
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Normally this is None, unless triggered
                trigger = self.current_scene.handle_events(event)
                
                if trigger is not None:
                    # Scene Switches
                    if trigger == "Title":
                        self.current_scene = TitleScene(self.screen, self.config)
                        self.title = "Mayhem (Main Menu)"
                    elif trigger == "Game":
                        self.current_scene = Mayhem(self.screen, self.config)
                        self.title = "Mayhem"
                    elif trigger == "Settings":
                        self.current_scene = Settings(self.screen, self.config)
                        self.title = "Mayhem (Settings)"
                    elif trigger == "Egg":  # Easter egg
                        self.config["background"] = "Assets/Backgrounds/Garlic.PNG"
                    
                    # If it's not a scene switch it's a config change
                    else:
                        key, val = trigger
                        self.config[key] = val
                        
                        # Checking for screen changes or full screen flagging
                        if key in ["res_change", "full_screen"]:
                            if key == "res_change":
                                self.config["screen_width"], self.config["screen_height"] = val
                            
                            # Rescaling the screen
                            self._apply_display_settings()
                    
                    # Updating caption
                    pygame.display.set_caption(self.title)
       
    def run(self) -> None:
        """
        Running unless stopped
        """
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self._event_handler()
            self.current_scene.update(dt)
            self.current_scene.draw()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()