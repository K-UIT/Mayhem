"""Collection of sprite classes used to generate the world, so stars, planets and fuelbarrels"""

import pygame, random, math

class Stars(pygame.sprite.Sprite):
    def __init__(self, bounds: tuple, number: int, layer: int, flicker: bool = True):
        super().__init__()
        self._layer  = layer
        self.bounds  = bounds
        self.flicker = flicker
        
        # Generation Logic
        self.star_data = []
        for _ in range(number):
            self.star_data.append({
                "pos"       : pygame.Vector2(random.randint(0, int(bounds[0])), random.randint(0, int(bounds[1]))),
                "alpha"     : random.randint(0, 255),  # Transparency
                "speed"     : random.uniform(50, 150), # Flicker speed
                "direction" : random.choice([-1, 1]),  # Fading in or out
                "size"      : random.randint(1, 3)})

        # Creating the star surface, gets scaled later on
        self.base_star_surf = pygame.Surface((3, 3), pygame.SRCALPHA)
        self.base_star_surf.fill((255, 255, 255))
        

        self.image = pygame.Surface(bounds, pygame.SRCALPHA)
        self.rect  = self.image.get_rect()

    def update(self, dt: float) -> None:
        """
        Only used if flickering, do not need for static stars
        """
        if not self.flicker: return

        # Clear the massive surface with transparent overlay
        self.image.fill((0, 0, 0, 0)) 
        
        # Updating each star
        for star in self.star_data:
            # Updating transparency depending on speed and direction
            star["alpha"] += star["speed"] * dt * star["direction"]
            
            # Flip direction to fade out if we're over the maximum alpha
            if star["alpha"] >= 255:
                star["alpha"]     = 255
                star["direction"] = -1
                
            # If we're at the minimum alpha value then we flip the direction to fade in
            elif star["alpha"] <= 0:
                star["alpha"]     = 0
                star["direction"] = 1
                
                # Teleport star to new random spot when it goes fully dark
                star["pos"] = pygame.Vector2(random.randint(0, int(self.bounds[0])), random.randint(0, int(self.bounds[1])))

            # Scaling the star up and adding it to the background
            star_surf = pygame.transform.scale(self.base_star_surf, (star["size"], star["size"]))
            star_surf.set_alpha(star["alpha"])
            self.image.blit(star_surf, star["pos"])

    def draw_visible_stars(self, target_surface : pygame.Surface, camera_offset : tuple, camera_size : tuple) -> None:
        """
        Only for static stars, not flickering ones
        """
        if self.flicker: return
        
        # Getting the current view size
        view_rect = pygame.Rect(camera_offset.x, camera_offset.y, camera_size[0], camera_size[1])
        
        # Going through each star
        for star in self.star_data:
            # Only drawing the visible ones to save processing power
            if view_rect.collidepoint(star["pos"]):
                # Scaling and setting alpha
                star_surf = pygame.transform.scale(self.base_star_surf, (star["size"], star["size"]))
                star_surf.set_alpha(star["alpha"])
                
                # Adding star to the surface
                screen_pos = star["pos"] - camera_offset
                target_surface.blit(star_surf, screen_pos)
                
                

class FuelBarrel(pygame.sprite.Sprite):
    """
    Fuel barrel sprite class
    """
    # Class variables to share the rotated image across ALL barrel objects, to save processing
    base_image     = None
    rotated_image  = None
    rotation_angle = 0

    def __init__(self, position : tuple, layer : int = 0, config : dict = None):
        super().__init__()
        self._layer = layer
        self.config = config
        
        # Loading image once
        if FuelBarrel.base_image is None:
            FuelBarrel.base_image    = pygame.image.load("Assets/Sprites/Fuel.PNG").convert_alpha()
            FuelBarrel.base_image    = pygame.transform.scale(FuelBarrel.base_image, (30, 30))
            FuelBarrel.rotated_image = FuelBarrel.base_image

        self.image = FuelBarrel.rotated_image
        self.rect  = self.image.get_rect(center=position)
        self.pos   = pygame.Vector2(position)

    @classmethod
    def update_rotation(cls, dt: float) -> None:
        """
        This gets called one time per frame in the main loop, instead of 50 times
        Rotates the image
        """
        cls.rotation_angle = (cls.rotation_angle + 100 * dt) % 360
        cls.rotated_image  = pygame.transform.rotate(cls.base_image, cls.rotation_angle)

    def draw(self, surface : pygame.Surface, offset : tuple) -> None:
        """
        Using the shared rotated image and drawing it on the surface
        """
        rect = self.rotated_image.get_rect(center=self.pos - offset)
        surface.blit(self.rotated_image, rect)
        
    
    
class Planet(pygame.sprite.Sprite):
    """
    Planet sprite class, used for moving planets and calculating gravity
    While this is a planet class it is also used for stars and white holes, so "celestial body" might have been a more apropriate name haha
    """
    # Universal gravitational constant, this is what gets tweaked when changing gravity in the settings
    G = 1e-1
    def __init__(self, sun_pos: tuple, name: str, orbit_radius: int, size: int, orbit_speed: int, rotation_speed: int, layer: int, 
                 mass: int, touch : str = "bump", shrink : float = 1, config : dict = None):
        super().__init__()
        self._layer = layer
        self.config = config
        self.name   = name
        self.mass   = mass
        self.touch  = touch
        self.radius = size // 2
        self.shrink = shrink
        
        # Loading in the sprite image that will rotate and orbit and such, and scaling it up
        self.original_image = pygame.image.load(f"Assets/Planets/{name}.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (size, size))
        self.image          = self.original_image.copy()
        
        # Making a circular mask that moves with the image, most of the planets aren't perfect circles but this works fine
        mask_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask_surf, (255, 255, 255), (self.radius, self.radius), self.radius * self.shrink)
        self.mask = pygame.mask.from_surface(mask_surf)
        
        # Making a hitbox
        self.hitbox_rect = pygame.Rect(0, 0, size, size)
        
        # Starting variables
        self.sun_pos        = pygame.Vector2(sun_pos)
        self.orbit_radius   = orbit_radius
        self.orbit_speed    = orbit_speed / self.config["orbit_speed_mult"]
        self.orbit_angle    = random.randint(0, 360)
        self.rotation_speed = rotation_speed * self.config["planet_rot_speed_mult"]
        self.rotation_angle = 0
        
        # Positional updating
        self.pos = pygame.Vector2(0, 0)
        self._update_position(0)
        
        self.rect               = self.image.get_rect(center=self.pos)
        self.hitbox_rect.center = self.pos

    def _update_position(self, dt : float) -> None:
        """
        Updating the orbit position
        """
        # If we have an orbit speed, then we update the orbit angle
        if self.orbit_speed > 0: self.orbit_angle += (360 / self.orbit_speed) * dt
        rad      = math.radians(self.orbit_angle)
        offset   = pygame.Vector2(math.cos(rad), math.sin(rad)) * self.orbit_radius
        self.pos = self.sun_pos + offset

    def update(self, dt : float) -> None:
        """
        Updating position and rotation every frame
        """
        # Updating position
        self._update_position(dt)
        
        # Rotating the image for visuals only
        self.rotation_angle += self.rotation_speed * dt
        self.image           = pygame.transform.rotate(self.original_image, self.rotation_angle)
        
        # Update the drawing rect 
        self.rect = self.image.get_rect(center=self.pos)
        
        # Update the hitbox rect 
        self.hitbox_rect.center = self.pos

    def get_gravity_acceleration(self, ship_pos: pygame.Vector2) -> pygame.Vector2:
        """
        Returns the acceleration vector relative to the ship
        Calculated using the force applied from the planet to the ship (assuming ships weight unit is 1 for simplicity)
        """
        
        direction = self.pos - ship_pos
        distance  = direction.length()
        if distance < 5: return pygame.Vector2(0, 0) # If too close then set acceleration to 0
        
        # Gravity formula g=GM/r^2, because of how this is done it allows for negative mass
        magnitude = (Planet.G * self.mass) / (distance ** 2)
        return direction.normalize() * magnitude
    
    def draw(self, surface : pygame.Surface, offset : tuple) -> None:
        """
        Drawing the planet onto the surface
        """
        rect = self.image.get_rect(center=self.pos - offset)
        surface.blit(self.image, rect)