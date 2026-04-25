"""Config file where hard coded starting variables chan be easily changed
They can of course also be edited in game using the settings menu! Though not all can be changed in game"""

"""WARNING, CHANGING SOME OF THE STUFF LIKE FPS BREAKS THE GAME, BE CAREFUL!"""

Configure = {
    # General screen stuff
    "screen_width"  : 1280,
    "screen_height" : 720,
    "full_screen"   : False,
    
    # Refresh rate
    "fps" : 60,
    
    # Starting screen
    "start" : "Main Menu", # only "Main Menu", "Game" and "Settings" are valid
    
    # Main menu letter moving logic
    "amplitude" : 10,
    "frequency" : 3,
    
    # Global background
    "background" : "Assets/Backgrounds/MainMenu.JPG", 
    
    # World physics
    "gravity_multiplier"    : 1.0,
    "orbit_speed_mult"      : 1.0,
    "planet_rot_speed_mult" : 1.0,
    "friction"              : 0.5,       
    
    # Ship modifiers
    "thrust_power"   :  500,
    "fuel_decay"     :    3,
    "bullet_speed"   : 3000,
    "start_fuel"     :  100,
    "rotation_speed" :  180,
    "cooldown"       :   1, 
    
    # Fuel barrels
    "barrel_fuel_value": 20,
    "barrel_count"     : 50,
    
    # Number of stars
    "star_count" : 3000,
    
    # Permanant on screen map
    "perm_map" : False,
    
    # -Character classes and colors-
    "p1_ship_class" : "fighter", # Only fighter, cruiser and destroyer are valid classes
    "p2_ship_class" : "fighter",
    "p1_ship_color" : "blue",    # Only red, blue, green and pink are valid colors
    "p2_ship_color" : "red",
    
    # Fighter
    "fighter_thrust"       : 0,
    "fighter_fuel_decay"   : 0,
    "fighter_bullet_speed" : 0,
    "fighter_rotation"     : 0,
    "fighter_friction"     : 0,
    "fighter_cooldown"     : 0,
    
    # Cruiser
   "cruiser_thrust"       : 100,
   "cruiser_fuel_decay"   :   2,
   "cruiser_bullet_speed" : 500,
   "cruiser_rotation"     :  40,
   "cruiser_friction"     :-0.2,
   "cruiser_cooldown"     :-0.5,
   
   # Destroyer
   "destroyer_thrust"       : -100,
   "destroyer_fuel_decay"   :   -1,
   "destroyer_bullet_speed" : -500,
   "destroyer_rotation"     :  -40,
   "destroyer_friction"     :  0.2, 
   "destroyer_cooldown"     :  0.5,
   
}   