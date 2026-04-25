"""Settings menu where different things can be changed globally"""
import pygame
from ..Helpers import BaseScene
from ..Sprites import Image, Text, Button

class Settings(BaseScene):
    def __init__(self, screen : object, config : dict):
        """
        Setting up elements that do not change and state logic
        """
        super().__init__(screen)
        self.config = config
        
        # -Groups-
        self.base_sprites = pygame.sprite.LayeredUpdates() 
        self.active_group = pygame.sprite.LayeredUpdates() 
        self.input_group  = pygame.sprite.LayeredUpdates() 
        
        # Tracking current category
        self.current_category = "General"
        self.orange = (233, 119, 57)
        
        # Setting up initial layout
        self.setup_layout()
        
        # Input logic states
        self.input_mode = None  
        self.user_text = ""
        self.temp_val = None 
        
    def setup_layout(self) -> None:
        """
        Setting up relative sizing, and defining where everything should be
        """
        self.base_sprites.empty()
        self.active_group.empty()
        
        # -Background and dark overlay-
        self.bg = Image(self.config["background"], (0,0), layer = 0, size = (self.screen_width, self.screen_height), blur = 5)
        
        self.dark_overlay = Button((0,0), (self.screen_width, self.screen_height), (0,0,0,150), layer = 1, message="Overlay")
        
        # -Title Section-
        title_font = self.screen_height // 8
        self.title = Text("Settings", (self.screen_width // 2, self.screen_height * 0.08), layer = 2, size = title_font, anchor = "center")
        self.title_line = Button((self.screen_width * 0.1, self.screen_height * 0.15), (self.screen_width * 0.8, self.screen_height * 0.01), 
                                 color = self.orange, layer = 2, radius = 50)

        # -Category Tabs-
        tab_names = ["General", "Physics", "Ship", "World", "Class"]
        tab_width = (self.screen_width * 0.8) // len(tab_names)
        self.tab_buttons = []
        
        for i, name in enumerate(tab_names):
            x_pos = (self.screen_width * 0.1) + (i * tab_width)
            col = self.orange if self.current_category == name else "white"
            btn = Button((x_pos, self.screen_height * 0.17), (tab_width * 0.9, self.screen_height * 0.05), (0,0,0,0), layer = 2, text = name, 
                         txt_size = self.screen_height//25, txt_color = col, message = f"TAB_{name}", outline_col = (col, col))
            self.tab_buttons.append(btn)
        
        # Addubg all sprites to a group
        self.base_sprites.add(self.bg, self.dark_overlay, self.title, self.title_line, self.tab_buttons)
        
        # Calling for tab specific sprites
        self._load_category_sprites()

    def _load_category_sprites(self) -> None:
        """
        Helper to spawn the specific buttons for the current tab
        """
        # Clearing active group
        self.active_group.empty()
        
        # Sizing
        label_x, row_x = self.screen_width * 0.1, self.screen_width * 0.35
        btn_dim = (self.screen_width // 10, self.screen_height // 14)
        
        # All the different buttons for the different tabs
        content = []
        if self.current_category == "General":
            content = [("Resolution", "res_change",  ["720p", "1080p", "800x600"]),
                       ("Fullscreen", "full_screen", [True, False])]
            
        elif self.current_category == "Physics":
            content = [("Gravity",         "gravity_multiplier",    [0.5, 1.0, 2.0]),
                       ("Orbit Speed",     "orbit_speed_mult",      [0.5, 1.0, 2.0]),
                       ("Planet Rotation", "planet_rot_speed_mult", [0.5, 1.0, 2.0]),
                       ("Friction",        "friction",              [0.0, 0.5, 1.0])]
            
        elif self.current_category == "Ship":
            content = [("Thrust Power",    "thrust_power",  [300, 500, 800]),
                       ("Fuel Decay",      "fuel_decay",    [1, 3, 5]),
                       ("Bullet speed",    "bullet_speed",  [1000, 3000, 5000]),
                       ("Starting Fuel",   "start_fuel",    [50, 100, 200]),
                       ("Rotation Speed", "rotation_speed", [90, 180, 220])]
            
        elif self.current_category == "World":
            content = [("Number Of Barrels", "barrel_count",      [20, 50, 100]),
                       ("Fuel Per Barrel",   "barrel_fuel_value", [10, 20, 50]),
                       ("Number Of Stars",   "star_count",        [1000, 3000, 5000]),
                       ("Map Always On",     "perm_map",          [True, False])]
        
        elif self.current_category == "Class":
            content = [("Player 1 Class", "p1_ship_class",      ["fighter", "cruiser", "destroyer"]),
                       ("Player 2 Class", "p2_ship_class",      ["fighter", "cruiser", "destroyer"]),
                       ("Player 1 Color", "p1_ship_color",      ["blue", "red", "green", "pink"]),
                       ("Player 2 Color", "p2_ship_color",      ["blue", "red", "green", "pink"])]
        # Adding content to sprite group
        for i, (label, key, options) in enumerate(content):
            y_pos = self.screen_height * (0.3 + (i * 0.15))
            
            # Adding label text
            self.active_group.add(Text(label, (label_x, y_pos), layer=2, size=self.screen_height//25))
            
            # Adding a custom buttons to everything but the True/False options
            is_bool  = len(options) > 0 and isinstance(options[0], bool)
            is_class = len(options) > 0 and "class" in key
            is_col   = len(options) > 0 and "color" in key
            btn_list = options if is_bool or is_class or is_col else options + ["Custom"]
            
            # Buttom generation and current state setup
            for n, val in enumerate(btn_list):
                is_active = False
                
                # Decoding what the resolution buttons mean
                if key == "res_change":
                    res_map     = {"720p": (1280, 720), "1080p": (1920, 1080), "800x600": (800, 600)}
                    current_res = (self.config.get("screen_width"), self.config.get("screen_height"))
                    if val in res_map: 
                        is_active = (current_res == res_map[val])
                    elif val == "Custom":
                        is_active = (current_res not in res_map.values())
                else:
                    current_val = self.config.get(key)
                    if val == "Custom":
                        is_active = (current_val not in options)
                    else:
                        is_active = (current_val == val)
                
                # Glowing selected buttons
                border = ("white", (233, 189, 57)) if is_active else ("white", self.orange)
                
                # Making the buttons
                b = Button((row_x + n * btn_dim[0]*1.1, y_pos - btn_dim[1]//4), btn_dim, (0,0,0,0), 
                           layer=3, text=str(val), txt_size=self.screen_height//25, txt_color=self.orange,
                           message=(key, val), outline_col=border)
                self.active_group.add(b)

    def handle_events(self, event : object) -> any:
        """
        Process inputting of text, pressing buttons and optionally return the next scene
        """
        if event.type == pygame.KEYDOWN:
            
            # Typing logic
            if self.input_mode:
                if event.key == pygame.K_RETURN:
                    res = self._process_custom_input()
                    if self.input_mode is None: 
                        self.input_group.empty() 
                        self.setup_layout()
                    return res
                
                # Hitting backspace
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                
                # Only accepting digits or decimal points if that is allowed
                elif event.unicode.isdigit() or (event.unicode == "." and "multiplier" in str(self.input_mode)):
                    self.user_text += event.unicode
                
                self._update_input_prompt()
                return None
            
            # Scene return triggers
            if event.key == pygame.K_ESCAPE: return "Title"
            if event.key == pygame.K_p:      return "Game"
        
        # Decoding what mouse clicks mean
        if event.type == pygame.MOUSEBUTTONDOWN and not self.input_mode:
            
            msg = self.dark_overlay.is_clicked(event.pos)
            
            # If the background has more than 10 clicks trigger the easter egg
            if msg == "Overlay":
                if self.dark_overlay.clicks >= 10:
                    self.dark_overlay.clicks = 0
                    return "Egg"
            
            # Tab changes
            for btn in self.tab_buttons:
                msg = btn.is_clicked(event.pos)
                if msg and "TAB_" in msg:
                    self.current_category = msg.replace("TAB_", "")
                    self.setup_layout()
                    return None
            
            # Current active buttons
            for btn in list(self.active_group):
                if isinstance(btn, Button): # Only checking buttons for button clicks
                    trigger = btn.is_clicked(event.pos)
                    if trigger:
                        key, val = trigger
                        
                        # Entering custom mode
                        if val == "Custom":
                            self.input_mode = key
                            self.user_text = ""
                            
                            self.input_group.empty()
                            self.dark_overlay2 = Button((0,0), (self.screen_width, self.screen_height), (0,0,0,200), layer = 9)
                            self.input_sprite = Text("", (self.screen_width//2, self.screen_height//2), 
                                                     layer=10, size=self.screen_height//15, color="white", anchor="center")
                            self.input_group.add(self.dark_overlay2, self.input_sprite)
                            self._update_input_prompt()
                            return None
                        
                        # Decoding res changes 
                        if key == "res_change":
                            res_map = {"720p": (1280, 720), "1080p": (1920, 1080), "800x600": (800, 600)}
                            return ("res_change", res_map[val])
                        
                        # Updating preset configs
                        self.config[key] = val
                        self.setup_layout() 
                        return (key, val)

    def update(self, dt : float) -> None:
        """
        Updating all sprites
        """
        for s in list(self.base_sprites) + list(self.active_group) + list(self.input_group):
            s.update()
    
    def _update_input_prompt(self) -> None:
        """
        Updates the text on screen depending on what step of input we are in
        """
        # Custom res change input mode (since it takes 2 inputs)
        if self.input_mode == "res_change":
            txt = "Width" if self.temp_val is None else "Height"
            self.input_sprite.update_text(f"Enter Resolution {txt}: {self.user_text}")
        
        # Generic input mode for custom button click
        else:
            clean_name = self.input_mode.replace("_", " ").title()
            self.input_sprite.update_text(f"Enter {clean_name}: {self.user_text}")

    def _process_custom_input(self) -> any:
        """
        Custom logic for text entry
        """
        try:
            # Two stage input mode for resolution change
            if self.input_mode == "res_change":
                if self.temp_val is None:
                    self.temp_val = int(self.user_text)
                    self.user_text = ""
                    self._update_input_prompt()
                    return None
                else: 
                    res = (self.temp_val, int(self.user_text))
                    self.temp_val = None
                    self.input_mode = None
                    return ("res_change", res)
            
            # Single stage input for everything else
            else:
                val = float(self.user_text) if "." in self.user_text else int(self.user_text)
                key = self.input_mode
                self.input_mode = None
                self.config[key] = val
                return (key, val)
        
        # Set errors as blank
        except ValueError:
            self.user_text = ""
            self._update_input_prompt()

    def draw(self) -> None:
        """
        Drawing all groups
        """
        self.base_sprites.draw(self.screen)
        self.active_group.draw(self.screen)
        self.input_group.draw(self.screen)