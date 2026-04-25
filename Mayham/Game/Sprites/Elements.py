"""Collection of sprite classes used for general game elements, buttons, text and so on, also has the world map"""
import pygame, math

class Image(pygame.sprite.Sprite):
    """
    Generic sprite class for images
    """
    def __init__(self, image_path : str, position : tuple, layer : int, size : tuple, blur : int = 0):
        super().__init__()
        self.image  = pygame.image.load(image_path).convert_alpha()
        self._layer = layer 
        
        # Adding blur to the image
        if blur:
            bg_size = self.image.get_size()
            
            # Downscale then upscale to create a smooth blur effect
            small_surf = pygame.transform.smoothscale(self.image, (bg_size[0]//blur, bg_size[1]//blur))
            self.image = pygame.transform.smoothscale(small_surf, bg_size)
            
        self.image = pygame.transform.scale(self.image, size)  
        self.rect  = self.image.get_rect(topleft=position)           



class Text(pygame.sprite.Sprite):
    """
    Sprite for static and dynamic text
    """
    def __init__(self, text : str, position : tuple, layer : int, size : int, color : tuple = (233, 119, 57) , 
                 font_path  : str = "Assets/pokemon_font.ttf",  anchor : str = "topleft"):
        super().__init__()
        self.color  = color
        self._layer = layer
        self.text   = text
        self.pos    = position
        self.anchor = anchor
        self.font   = pygame.font.Font(font_path, size)
        self.image  = self.font.render(text, True, self.color)
        self.rect   = self.image.get_rect(**{self.anchor: position})

    def update_text(self, new_text : str, position : tuple = None, color : str = None) -> None:
        """
        Updating text, position and color
        """
        new_text = new_text if new_text is not None else self.text
        new_pos  = position if position is not None else self.pos
        new_col  = color    if color    is not None else self.color
        
        self.image  = self.font.render(new_text, True, new_col)
        self.rect   = self.image.get_rect(**{self.anchor: new_pos})



class Button(pygame.sprite.Sprite):
    """
    Sprite maker for clickable buttons, doubles as a square maker if nothing is filled in!
    """
    def __init__(self, position: tuple, dimensions: tuple, color: tuple, layer : int, 
                 radius : int = 5, txt_color : tuple | str = "white", txt_size : int = 0, message : any = None,
                 text : str  = "", outline_col : tuple = False, font_path: str = "Assets/pokemon_font.ttf"):
        super().__init__()
        self._layer  = layer
        self.pos     = position
        self.dim     = dimensions
        self.radius  = radius
        self.message = message
        self.clicks  = 0
        self.out_col = outline_col

        # Pre rendering the text surface
        font = pygame.font.Font(font_path, txt_size)
        self.text_surf = font.render(text, True, txt_color)

        # Generate two states (hover and not hover)
        self.image_normal = self._create_surf(color, outline_col, is_hover=False)
        self.image_hover  = self._create_surf(color, outline_col, is_hover=True) 

        self.image = self.image_normal
        self.rect  = self.image.get_rect(topleft=position)

    def _create_surf(self, color : str, outline_col : tuple, is_hover : bool) -> object:
        """
        Button maker
        """
        surf = pygame.Surface(self.dim, pygame.SRCALPHA)

        if outline_col:
            # If hovering, force the outline to color 2, otherwise use the outline color
            current_outline = outline_col[0] if is_hover else outline_col[1]
            
            # Draw outline
            pygame.draw.rect(surf, current_outline, (0, 0, self.dim[0], self.dim[1]), border_radius=self.radius)
            
            # Draw inner surface
            pygame.draw.rect(surf, color, (4, 4, self.dim[0]-8, self.dim[1]-8), border_radius=self.radius)
        else:
            # No outline version
            pygame.draw.rect(surf, color, (0, 0, self.dim[0], self.dim[1]), border_radius=self.radius)

        # Center and blit the pre rendered text
        text_rect = self.text_surf.get_rect(center=(self.dim[0]//2, self.dim[1]//2))
        surf.blit(self.text_surf, text_rect)
        
        return surf

    def update(self, dt : float = 0) -> None:
        """
        Changing button state based on mouse position
        """
        mouse_pos  = pygame.mouse.get_pos()
        self.image = self.image_hover if self.rect.collidepoint(mouse_pos) else self.image_normal

    def is_clicked(self, mouse_pos: tuple) -> tuple | float | bool:
        """
        Looking for click events
        """
        if self.rect.collidepoint(mouse_pos):
            self.clicks += 1 # Counting up by 1
            return self.message if self.message is not None else True
        return False
    
    def resize(self, percentage: float):
        """
        Resizes the buttonss image based on a given percentage
        """
        percentage = max(0, min(1, percentage))
        new_width  = int(self.dim[0] * percentage)
        new_surf   = pygame.Surface(self.dim, pygame.SRCALPHA)
        
        # Adding outline
        pygame.draw.rect(new_surf, self.out_col[1], (0, 0, self.dim[0], self.dim[1]), border_radius=self.radius)
        pygame.draw.rect(new_surf, (30, 30, 30), (4, 4, self.dim[0]-8, self.dim[1]-8), border_radius=self.radius)
        
        # Adjust fuel fill to stay inside the outline
        fill_x, fill_y = 4, 4
        fill_w = max(0, new_width - 8)
        fill_h = self.dim[1] - 8
        
        # Changing color depending on fuel level
        if fill_w > 0:
            color = "red"
            if percentage   >= 0.65: color = "green"
            elif percentage >= 0.45: color = "yellow"
            elif percentage >= 0.20: color = "orange"
            
            pygame.draw.rect(new_surf, color, (fill_x, fill_y, fill_w, fill_h), border_radius=self.radius)
            
        self.image = new_surf



class MiniMap(pygame.sprite.Sprite):
    """
    Toggalable mini version of the world map, shows icons of all the planets and their current position
    Also shows the player locations
    """
    def __init__(self, size: int, world_size: tuple, planets, layer: int, screen_size: tuple, visible : bool = False):
        super().__init__()
        self._layer     = layer
        self.size       = size
        self.world_size = world_size
        self.scale      = size / world_size[0]
        self.sun_pos    = world_size[0] // 2
        self.image      = pygame.Surface((size, size), pygame.SRCALPHA)
       
        # Position the map in the center of the screen
        self.rect    = self.image.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
        self.visible = visible    # Controlling visibility
        
        # Preloading and scaling icons
        self.icons = {}
        for p in planets:
            img = pygame.image.load(f"Assets/Symbols/{p.name}.png").convert_alpha()
            icon_size = int(25 + p.radius * self.scale) if p.name != "Sun" else 40 
            self.icons[p.name] = pygame.transform.smoothscale(img, (icon_size, icon_size))

    def update_map(self, players : pygame.sprite.Group, planets : pygame.sprite.Group) -> None:
        """
        Update the map surface if visible
        """
        # Completely transparent image if hidden
        if not self.visible:
            self.image.fill((0, 0, 0, 0))
            return

        # Clear and draw background
        self.image.fill((0, 0, 0, 200))
        pygame.draw.rect(self.image, (255, 255, 255), [0, 0, self.size, self.size], 2)

        # The suns location
        map_sun_x, map_sun_y = self.size // 2, self.size // 2

        # Drawing planets and orbits
        for p in planets:
            if p.orbit_radius > 0:
                map_orbit_r = int(p.orbit_radius * self.scale)
                self._draw_dashed_circle(self.image, (100, 100, 100), (map_sun_x, map_sun_y), map_orbit_r)

            # Relative location of the planet
            map_x, map_y = int(p.pos.x * self.scale), int(p.pos.y * self.scale)
            
            # Icon of the planet
            #if self.icons[p.name]:
            self.image.blit(self.icons[p.name], self.icons[p.name].get_rect(center=(map_x, map_y)))

        # Drawing players
        for i, player in enumerate(players):
            # Only draw if player is within world bounds (Used because dead players get put out of bounds)
            if 0 <= player.pos.x <= self.world_size[0]:
                map_x, map_y = int(player.pos.x * self.scale), int(player.pos.y * self.scale)
                color = (0, 150, 255) if i == 0 else (255, 50, 50)
                
                # Simple triangle shape for player
                ship_size = 14
                temp_surf = pygame.Surface((ship_size, ship_size), pygame.SRCALPHA)
                pygame.draw.polygon(temp_surf, color, [(ship_size//2, 0), (0, ship_size), (ship_size, ship_size)])
                
                # Rotation
                rotated_ship = pygame.transform.rotate(temp_surf, player.angle)
                self.image.blit(rotated_ship, rotated_ship.get_rect(center=(map_x, map_y)))

    def _draw_dashed_circle(self, surface : pygame.Surface, color : tuple, center : tuple, radius : int, dash_length : int =4) -> None:
        """
        Custom function that draws a circle with dahsed lines to illustrate planet orbits
        """
        circumference = 2 * math.pi * radius
        num_segments  = int(circumference / (dash_length * 2))

        # Drawing a bit of the circle for each segment
        for i in range(num_segments):
            # Start and ending angle
            start_angle = (i * 2 * math.pi) / num_segments
            end_angle   = start_angle + (math.pi / num_segments)
    
            # Drawing line connecting start and end position
            start_pos = (center[0] + radius * math.cos(start_angle), center[1] + radius * math.sin(start_angle))
            end_pos   = (center[0] + radius * math.cos(end_angle),   center[1] + radius * math.sin(end_angle))
            pygame.draw.line(surface, color, start_pos, end_pos, 1)