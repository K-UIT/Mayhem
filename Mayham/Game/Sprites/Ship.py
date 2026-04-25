"""Collection of sprite classes used for the spaceship logic, so the ship, the camera that follows the ship, and blasts the ship fires out"""
import pygame, math, random
from .Elements import Button

class Spaceship(pygame.sprite.Sprite):
    """
    Class for spaceships sprites with physics and rotation logic
    """
    def __init__(self, position : tuple, sprite_name : str, layer : int, size : tuple = (65, 65), config : dict = None):
        super().__init__()
        self.config    = config
        self._layer    = layer
        self.sprt_name = sprite_name
        
        # Character class and color
        self.char_class = self.config[self.sprt_name + "_class"]
        self.color      = self.config[self.sprt_name + "_color"]
        
        # Physics and state using vectors
        self.pos   = pygame.Vector2(position)
        self.vel   = pygame.Vector2(0, 0)
        self.angle = 0 
        
        # Constants with added class modifiers
        self.thrust_power   = self.config["thrust_power"]   + self.config[self.char_class + "_thrust"]
        self.rotation_speed = self.config["rotation_speed"] + self.config[self.char_class + "_rotation"]
        self.friction       = self.config["friction"]       + self.config[self.char_class + "_friction"]
        self.fuel_decay     = self.config["fuel_decay"]     + self.config[self.char_class + "_fuel_decay"]
        self.clss_cooldown  = self.config["cooldown"]       + self.config[self.char_class + "_cooldown"]
        self.cooldown       = 0
        self.heath          = 1 if self.char_class != "destroyer" else 3
        
        # Starting variables
        self.fuel  = self.config["start_fuel"]
        self.score = 0
        
        # Landing logic
        self.landed_on      = None  # Reference to the planet we are stuck to
        self.relative_angle = 0     # Our position relative to the planet's center
        
        # Thrusting logic
        self.thruster_img = pygame.image.load(f"Assets/Effects/{sprite_name}/thrust.png").convert_alpha()
        self.is_thrusting = False
        
        # Store the original image so rotation doesn't ruin quality
        self.original_image = pygame.image.load(f"Assets/Sprites/{self.char_class}/{self.color}.PNG").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, size)
        
        # Setting up image
        self.image = self.original_image.copy()
        self.rect  = self.image.get_rect(center=position)
        self.mask  = pygame.mask.from_surface(self.image)
        
        
    def handle_input(self, keys : list[bool], up : int, left : int, right : int, dt : float) -> None:
        """
        Handling rotation and thrust based on provided key mapping
        """
        # Rotation
        if keys[left]:  self.angle += self.rotation_speed * dt
        if keys[right]: self.angle -= self.rotation_speed * dt
        
        self.is_thrusting = False
        
        # Thrusting logic
        if keys[up] and self.fuel>0:
            # Launching away from landed planet
            if self.landed_on:
                self.landed_on = None
                launch_dir     = pygame.Vector2(0, -1).rotate(-self.angle)
                self.vel       = launch_dir * 200
            else:
                # Movement logic
                theta = math.radians(-self.angle)
                
                # Rotation mapping formula
                ax_initial, ay_initial = 0, -1
                ax = ax_initial * math.cos(theta) - ay_initial * math.sin(theta)
                ay = ax_initial * math.sin(theta) + ay_initial * math.cos(theta)

                # Increasing acceleration and velocity when thrusting
                acceleration      = pygame.Vector2(ax, ay) * self.thrust_power
                self.vel         += acceleration * dt
                self.fuel        -= self.fuel_decay * dt
                self.is_thrusting = True
                
    def _draw_thruster(self, surface : pygame.Surface, camera_offset) -> None:
        """
        Drawing relative thruster sprites
        """
        # Only draw if we are thrusting
        if self.is_thrusting:
            # Rotating sprite with ship
            rotated_thruster = pygame.transform.rotate(self.thruster_img, self.angle + 90)
            
            # Getting the vector pointing backwards from the ship
            thrust_direction = pygame.Vector2(0, 1).rotate(-self.angle)
            
            # Adjusting where the thruster effect comes out from
            distance_from_center = 50 
            thruster_world_pos = self.pos + (thrust_direction * distance_from_center)
            
            # Adding a jittering scaling effect, for some movement
            pulse = random.uniform(0.9, 1.1)
            w, h = rotated_thruster.get_size()
            # Scale the rotated image for the pulse
            final_thruster = pygame.transform.smoothscale(rotated_thruster, (int(w//2 * pulse), int(h//2 * pulse)))
            
            rect = final_thruster.get_rect(center=thruster_world_pos - camera_offset)
            surface.blit(final_thruster, rect)
    
    def shoot(self) -> object:
        """
        Shooting logic with cooldown
        """
        if self.cooldown>=self.clss_cooldown:
            self.cooldown = 0
            rad       = math.radians(-self.angle + 90) # Match the ships rotation
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            spawn_pos = self.pos - (direction * 40) 
        
            return Blast(spawn_pos, self.angle, self._layer - 1, self.vel, self.sprt_name, self, self.config)
        
        return None

    def update(self, dt : float) -> None:
        """
        Updating position and handling rotation
        """
        self.cooldown += dt
        
        # Rotating and moving with the planet
        if self.landed_on:
            current_total_angle = self.landed_on.rotation_angle + self.relative_angle
            rad = math.radians(current_total_angle)

            planet_surface = self.landed_on.radius * self.landed_on.shrink
            ship_offset = 5 # Small offset from the planet

            # DIstance from the planets hitbox
            dist = planet_surface + ship_offset
            
            self.pos.x, self.pos.y = self.landed_on.pos.x + math.cos(rad) * dist, self.landed_on.pos.y - math.sin(rad) * dist
            
            # Forcing the sprite to point directly away from the planets center
            self.angle = current_total_angle - 90 
            
            # Refuel logic
            self.fuel = min(100, self.fuel + 5 * dt)
            
            # Updating the image and rect so it doesn't flicker or disappear
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
        
        # Rotating and position logic when flying
        else:
            # Update position via velocity formula
            self.pos += self.vel * dt
            
            # Adding a hard coded world border that cannot be moved past
            # Checking x value
            if self.pos.x <= 0:
                self.pos.x = 0
                if self.vel.x < 0: self.vel.x = 0
            elif self.pos.x >= 10000:
                self.pos.x = 10000
                if self.vel.x > 0: self.vel.x = 0

            # Checking y value
            if self.pos.y <= 0:
                self.pos.y = 0
                if self.vel.y < 0: self.vel.y = 0
            elif self.pos.y >= 10000:
                self.pos.y = 10000
                if self.vel.y > 0: self.vel.y = 0
            
            # Applying friction if moving
            if self.vel.length() > 0: self.vel -= self.vel * self.friction * dt
            
            # Rotating the image
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect  = self.image.get_rect(center=self.pos)

    def draw(self, surface : object, camera_offset : tuple) -> None:
        """
        Draw the ship and thruster effect adjusted by the camera position
        """
        # Drawing the thruster behind the ship
        self._draw_thruster(surface, camera_offset)

        # Drawing the ship on top
        draw_pos  = self.pos - camera_offset
        draw_rect = self.image.get_rect(center=draw_pos)
        surface.blit(self.image, draw_rect)



class Blast(pygame.sprite.Sprite):
    # Loading once for each player at the class level, saces processing power
    images = {}

    def __init__(self, position: pygame.Vector2, angle: float, layer: int, velocity : pygame.Vector2, name, shooter : object, config : dict):
        super().__init__()
        self._layer  = layer
        self.pos     = pygame.Vector2(position)
        self.config  = config
        self.chr_cls = self.config[name + "_class"]
        self.speed   = self.config["bullet_speed"] + self.config[self.chr_cls + "_bullet_speed"]
        self.shooter = shooter
        
        
        # Determine which image to load based on the ship
        img_key = f"{name}/{self.chr_cls}"
        if img_key not in Blast.images: Blast.images[img_key] = pygame.image.load(f"Assets/Effects/{img_key}.png").convert_alpha()
        
        self.image = pygame.transform.rotate(Blast.images[img_key], angle + 90)
        self.rect  = self.image.get_rect(center=position)

        # Velocity vector
        self.vel = velocity + pygame.Vector2(math.sin(math.radians(angle)), math.cos(math.radians(angle))) * self.speed
        
    def update(self, dt: float) -> None:
        """
        Updating blast position and deleting stray blasts
        """
        # Moving the blast
        self.pos        -= self.vel * dt
        self.rect.center = self.pos

        # Delete if out of bounds or if hitting the world border
        if not (0 <= self.pos.x <= 10000 and 0 <= self.pos.y <= 10000):  self.kill()
            
    def draw(self, surface : pygame.Surface, offset : tuple):
        """
        Draw method for the camera to call
        """
        draw_pos = self.pos - offset
        
        # We use the rotated image created during initialization
        rect = self.image.get_rect(center=draw_pos)
        surface.blit(self.image, rect)



class Camera(pygame.sprite.Sprite):
    """
    A sprite that acts as a window or camera into the game
    """
    def __init__(self, position : tuple, size : tuple, layer : int, world_stars : object):
        super().__init__()
        self._layer      = layer
        self.size        = size
        self.image       = pygame.Surface(size)
        self.rect        = self.image.get_rect(center=position)
        self.world_stars = world_stars
        self.is_dead     = False
        
        # UI group
        self.ui_elements = pygame.sprite.LayeredUpdates()
        
        # Telling player how to respawn
        self.respawn_msg = Button((0, 0), (self.size[0], self.size[1]*1.2), (0, 0, 0, 0), 
            layer=11, text="Press shoot to respawn", txt_color="white", txt_size=self.size[0]//15)
        
        self.ui_elements.add(self.respawn_msg)
        
        self.death_msg = None
        
    def trigger_death(self, reason: str) -> None:
        """
        Draws the death reason on screen
        """
        self.is_dead = True
        
        # Removing death message
        if self.death_msg:
            self.ui_elements.remove(self.death_msg)
        
        # Death message written on a transparent button
        self.death_msg = Button((0, 0), (self.size[0], self.size[1]), (0, 0, 0, 160), 
                                layer=10, text=reason, txt_color=(255, 75, 75), txt_size=self.size[0]//10)

        # Add everything to the group to be drawn
        self.ui_elements.add(self.death_msg)
    
    def render_view(self, fuel_group : pygame.sprite.Group, ships : pygame.sprite.LayeredUpdates, 
                    blasts : pygame.sprite.Group, planets : pygame.sprite.Group, target : Spaceship) -> None:
        """
        Drawing everything that is currently on screen
        """
        # Making a black square
        self.image.fill((0, 0, 0)) 
        offset      = pygame.Vector2(target.pos.x - (self.size[0] // 2), target.pos.y - (self.size[1] // 2))
        camera_rect = pygame.Rect(offset.x, offset.y, self.size[0], self.size[1])

        # Adding stars
        self.world_stars.draw_visible_stars(self.image, offset, self.size)
        
        # Drawing all the sprites
        for sprite in list(planets) + list(fuel_group) + list(blasts) + list(ships):
            
            # Only drawing them if they're inside the cameras view
            if camera_rect.colliderect(sprite.rect):
                
                sprite.draw(self.image, offset) 
            
        # Death overlay
        if self.is_dead:
            self.ui_elements.draw(self.image)
