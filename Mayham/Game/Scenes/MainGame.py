"""Main game logic scene"""
import pygame, random, math

from ..Helpers import UI, BaseScene 
from ..Sprites import Image, Button, MiniMap, Stars, FuelBarrel, Planet, Spaceship, Camera 

class Mayhem(BaseScene):
    def __init__(self, screen: object, config: dict):
        """
        Setting up the world, planets, ships, and parsing global configs
        """
        super().__init__(screen)
        self.config       = config
        self.world_size   = (10000, 10000)
        sun_center        = ( 5000,  5000)
        orbit_scaler      = 5
        radius_scaler     = 1.5
        
        # -Gravitational constant-
        Planet.G = 1e-1 * self.config["gravity_multiplier"]
        
        # -Sprite groups-
        self.all_sprites  = pygame.sprite.LayeredUpdates()
        self.players      = pygame.sprite.LayeredUpdates()
        self.fuel_barrels = pygame.sprite.Group()
        self.blasts       = pygame.sprite.Group()
        self.planets      = pygame.sprite.Group()
        
        # -Background-
        self.bg = Image(self.config["background"], (0,0), layer = 0, size = (self.screen_width, self.screen_height), blur = 8)
        
        # -Dark overlay-
        self.overlay = Button((0,0), (self.screen_width, self.screen_height), (0,0,0,60), layer = 1, radius=0)
        
        # -World stars-
        self.world_stars = Stars(self.world_size, self.config["star_count"], layer=0, flicker = False)
        
        # -Camera-
        padding = self.screen_width * 0.05
        v_size  = (int((self.screen_width - (3 * padding)) // 2 * 0.9), int(self.screen_height * 0.85 * 0.6))
        
        self.vp1 = Camera((self.screen_width * 0.27, self.screen_height * 0.5), v_size, 3, self.world_stars)
        self.vp2 = Camera((self.screen_width * 0.73, self.screen_height * 0.5), v_size, 3, self.world_stars)
        
        # -Ship-
        self.p1 = Spaceship((random.randint( 100, 2300), random.randint(100, 9100)), "p1_ship", layer = 4, config=self.config)
        self.p2 = Spaceship((random.randint(2600, 9100), random.randint(100, 9100)), "p2_ship", layer = 4, config=self.config)
        
        # -Fuel barrels-
        self.fuel_barrels = pygame.sprite.Group()
        for _ in range(self.config["barrel_count"]):
            pos = (random.randint(0, 5000), random.randint(0, 5000))
            self.fuel_barrels.add(FuelBarrel(pos))#, config=self.config))
            
        # -UI- 
        self.ui = UI(screen, self.config, self.all_sprites)
        
        # -Planets-
        # The Sun 
        self.sun = Planet(sun_center, name = "Sun", orbit_radius = 0, size = 2 * 2001//orbit_scaler, orbit_speed = 0, rotation_speed = 10, layer=2, mass=4e8, touch = "kill", shrink = 0.9, config=self.config)
        
        # The rest of the planets
        self.Hour_Glass_Twins = Planet(sun_center, "HourGlassTwins", orbit_radius =  5000//orbit_scaler, size = 2 * 200 // radius_scaler, orbit_speed = 110, rotation_speed = 30, layer=2,  mass=3.2e6, touch = "bump", shrink = 0.5, config=self.config)
        self.Timber_Hearth    = Planet(sun_center, "TimberHearth",   orbit_radius =  8000//orbit_scaler, size = 2 * 250 // radius_scaler, orbit_speed = 250, rotation_speed = 20, layer=2,  mass=5.1e6, touch = "land", shrink = 0.5, config=self.config)
        self.Brittle_Hollow   = Planet(sun_center, "BrittleHollow",  orbit_radius = 12000//orbit_scaler, size = 2 * 300 // radius_scaler, orbit_speed = 397, rotation_speed = 30, layer=2,  mass=3.9e6, touch = "tele", shrink = 0.3, config=self.config)
        self.Giants_Deep      = Planet(sun_center, "GiantsDeep",     orbit_radius = 16500//orbit_scaler, size = 2 * 500 // radius_scaler, orbit_speed = 520, rotation_speed = 10, layer=2,  mass=2.2e7, touch = "land", shrink = 0.8, config=self.config)
        self.Dark_Bramble     = Planet(sun_center, "DarkBramble",    orbit_radius = 20000//orbit_scaler, size = 2 * 200 // radius_scaler, orbit_speed = 875, rotation_speed =  0, layer=2,  mass=3.2e6, touch = "kill", shrink = 0.3, config=self.config)
        self.White_Hole       = Planet(sun_center, "WhiteHole",      orbit_radius = 23000//orbit_scaler, size = 2 * 100 // radius_scaler, orbit_speed = 946, rotation_speed =  2, layer=2,  mass= -3e8, touch = "push", shrink = 0.8, config=self.config)
       
        # -Adding players and planet sprites to group-
        self.players.add(self.p1, self.p2)
        self.planets.add(self.sun, self.Hour_Glass_Twins, self.Timber_Hearth, self.Giants_Deep, self.Brittle_Hollow, self.White_Hole, self.Dark_Bramble)
          
       
        # -Minimap-
        downscale = 4 if self.config["perm_map"] else 1.5
        self.minimap = MiniMap(self.screen_height // downscale, self.world_size, self.planets, layer=10, screen_size=(self.screen_width, self.screen_height), visible = self.config["perm_map"])
        
        # -Adding world elements-
        self.all_sprites.add(self.bg, self.overlay, self.vp1, self.vp2, self.minimap)
        
    def handle_events(self, event : object) -> None|str:
        """
        Checking if we want to return to the main menu or settings menu
        Also trigger shooting, minimap and clicking the fuel bar
        """
        if event.type == pygame.KEYDOWN:
            # -Scene navigator-
            if event.key == pygame.K_p:      return "Settings"
            if event.key == pygame.K_ESCAPE: return "Title"
            
            # -Show minimap-
            if event.key == pygame.K_m: self.minimap.visible = True
            
            # -P1 shoot and respawn logic-
            if event.key == pygame.K_s: 
                if self.vp1.is_dead:
                    self.vp1.is_dead = False
                    self._respawn_player(self.p1)
                else:
                    new_blast = self.p1.shoot()
                    if new_blast: self.blasts.add(new_blast)
            
            # -P2 shoot and respawn logic-
            if event.key == pygame.K_DOWN: 
                if self.vp2.is_dead:
                    self.vp2.is_dead = False
                    self._respawn_player(self.p2)
                else:
                    new_blast = self.p2.shoot()
                    if new_blast: self.blasts.add(new_blast)
                    
        # -Hide minimap-
        if event.type == pygame.KEYUP and event.key == pygame.K_m and not self.config["perm_map"]: self.minimap.visible = False    
        
        # -UI buttons clicks-
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn, player in zip([self.ui.p1_fuel_bar, self.ui.p2_fuel_bar], self.players): # Checking all bars
                if btn.is_clicked(event.pos):
                    player.fuel += 1
                    
                    
    def update(self, dt: float) -> None:
        """
        Updating logic, handling inputs, collisions, and camera views
        """
        keys = pygame.key.get_pressed()
        
        # -Handling inputs-
        if not self.vp1.is_dead: self.p1.handle_input(keys, pygame.K_w,  pygame.K_a,    pygame.K_d,     dt)
        if not self.vp2.is_dead: self.p2.handle_input(keys, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, dt)            
        
        # -Updating elements-
        self.players.update(dt)
        self.planets.update(dt)
        self.blasts.update(dt)
        self.minimap.update_map(self.players, self.planets)
        FuelBarrel.update_rotation(dt)
        
        # -Updating camera-
        self.vp1.render_view(self.fuel_barrels, self.players, self.blasts, self.planets, self.p1)
        self.vp2.render_view(self.fuel_barrels, self.players, self.blasts, self.planets, self.p2)
        
        # -Collision logic-
        for player in self.players:
            if (player == self.p1 and self.vp1.is_dead) or (player == self.p2 and self.vp2.is_dead):
                continue
                
            # -Fuel barrel collision-
            for barrel in pygame.sprite.spritecollide(player, self.fuel_barrels, True):
                # Using configs for starting fuel caps and pickup amounts
                player.fuel   = min(self.config["start_fuel"], player.fuel + self.config["barrel_fuel_value"])
                player.score += 50
            
            # -Blast collision-
            for blast in pygame.sprite.spritecollide(player, self.blasts, False):
                if blast.shooter != player:
                    blast.kill()
                    player.heath -= 1
                    if player == self.p1 and player.heath <= 0: 
                        self.vp1.trigger_death("YOU WERE SHOT!")
                        self.p2.score += 200 # Award points to the shooter
                        player.pos = pygame.Vector2(-1000, -1000) 
                        player.vel = pygame.Vector2(0,0)
                        
                    elif player==self.p2 and player.heath <= 0:             
                        self.vp2.trigger_death("YOU WERE SHOT!")
                        self.p1.score += 200
                        player.pos = pygame.Vector2(-1000, -1000) 
                        player.vel = pygame.Vector2(0,0)
                        
            # -Planet collision and gravity-
            total_gravity = pygame.Vector2(0, 0)
            for planet in self.planets:
                
                # Removing blasts that hit planets
                pygame.sprite.spritecollide(planet, self.blasts, True)
                
                if player.rect.colliderect(planet.hitbox_rect):
                    offset = (player.rect.x - planet.hitbox_rect.x, player.rect.y - planet.hitbox_rect.y)
                    if planet.mask.overlap(player.mask, offset):
                        to_ship = (player.pos - planet.pos)
                        
                        # Figuring out if the planet is landable, pushes you away or will kill you (or teleport)
                        if planet.touch == "land" and player.vel.length()<500:
                            # Do not care about the entry speed, just lock the player to the planet
                            player.landed_on = planet
                            player.vel = pygame.Vector2(0, 0)
                            
                            impact_angle = math.degrees(math.atan2(-(player.pos.y - planet.pos.y), player.pos.x - planet.pos.x))
                            player.relative_angle = impact_angle - planet.rotation_angle
                            
                        elif planet.touch == "kill" or player.vel.length()>=500: 
                            if player == self.p1: self.vp1.trigger_death(f"Killed by: {planet.name}")
                            else:                 self.vp2.trigger_death(f"Killed by: {planet.name}")
                            
                            # Moving dead player off the map
                            player.pos = pygame.Vector2(-1000, -1000) 
                            player.vel = pygame.Vector2(0,0)
                        
                        elif planet.touch == "tele": 
                            player.pos = self.White_Hole.pos 
                        
                        else: 
                            push_dir = to_ship.normalize()
                            player.pos = planet.pos + (push_dir * (planet.radius + 15))
                            player.vel *= -0.2

                total_gravity += planet.get_gravity_acceleration(player.pos)
            
            player.vel += total_gravity * dt

        # -Bumping into another player-
        if pygame.sprite.collide_rect(self.p1, self.p2):
            
            push_direction = self.p1.pos - self.p2.pos
            
            # If they are at the exact same spot, provide a default push
            if push_direction.length() == 0:
                push_direction = pygame.Vector2(1, 0)
            
            # Normalize the push and move them apart
            push_direction = push_direction.normalize()
            
            # Flip velocities and add a "bounce" boost
            self.p1.vel =  push_direction * 300
            self.p2.vel = -push_direction * 300

        self.ui.update(self.players)

    def _respawn_player(self, player : Spaceship) -> None:
        """
        Resetting stats and putting player at a random spawn
        """
        player.score -= 100
        player.fuel   = self.config["start_fuel"]
        player.heath  = 1 if player.char_class != "destroyer" else 3
        player.vel    = pygame.Vector2(0, 0)
            
        # Set to a random start position
        player.pos = pygame.Vector2(random.randint(100, 4900), random.randint(100, 4900))
        
    def draw(self):
        """
        Drawing everything to screen
        """
        self.all_sprites.draw(self.screen)