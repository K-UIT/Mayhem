## READ ME
--------
# MAYHEM
--------

This is my Mayhem "clone", that is moreso a 2D outer wilds themed space shooter.
This is a VS style game, where two players play against eachother by controlling their own spaceships, 
while keeping track of their fuel, trying not to crash into planets and trying to shoot the other player.

All of the planet sprites were taken from this Pixilart post:                                     https://www.pixilart.com/art/solar-system-outer-wilds-sr29247997919aws3
The planet icons for the mini map were taken from the actual game, gathered in this Imgur folder: https://imgur.com/a/nomai-eye-symbols-Bc3pL2A
The ship sprites were taken from this free asset pack:                                            https://livingtheindie.itch.io/pixel-shmup-ships-free
And the fuel barrels were taken from megaman and edited by me to say F instead of E. Very original I know.
The UI was made by me by photobashing a bunch of free assets, and the backrounds were taken from free background pages.

To start the game, run main.py. Reading the following instructions is recommended.


--------
# CONTROLS
--------

Movement: 

Turning
To turn left and right, player 1 (p1) uses the A and D keys, while player 2 (p2) uses the left and right arrow keys. Turning speed is dependant on the players chosen character class. Some classes turn faster than others.

Thrust
To go forward, p1 presses W while P2 presses the arrow up key. You will know your ship is thrusting by seeing the flame effect behind the ship turn on. Thrust speed is effected by the players specific class' given thrust speed, and also how quickly you build up speed depends on how high your ships friction is.

## Of note regarding thrusting 
The speed limit is set at 500, this is moderetely fast, meaning if you have a speed that's too high and try to land on a planet you'll crash. Turn around and thrust away from the planet before landing to lessen your entry speed.

Shooting:
Shooting is done for p1 by pressing the S key, and for p2 by pressing the arrow down key. Shooting can be done while doing other actions. Different character classes have different recharge speeds, some take longer to recharge than others.


Other controls:

P key:
Press the P key while in the main game, or the settings screen to flip between main game and settings. This was meant to be a pause menu type thing, and could be made into one if a memory dictionary was made, which could be like the config dictionary. But there was not enough time to implement it fully.

M key:
Pressing and holding the M key while in the game will open a mini map. The mini map shows accurate positions for all planets and ships in the game. In the settings menu under the World tab, you can choose to have a smaller version of the map always be on screen, without needing to hold any buttons.  

Esc key:
Pressing the escape key while in the settings or main menu screen will send you back to the main menu. This means the game gets refreshed, and all scores get reset. 

Mouse:
The mouse is used to click on buttons in the game, like choosing to start the game or go into the settings in the main menu. It is also used to choose options in the settings menu. 
There are a few clicking related secrets in the game, like if you click on a fuel bar, it fills with 1 fuel per click. This was done to give an out in case fuel fully runs out. Clicking the background of the settings screen 10 times without interuptions, then going to the main menu might also do something, but I won't say what.


--------
# SCREENS
--------

There are 3 screen states in the game, that send the player between them. This explains each of them

## Main menu
--------
The main menu is the simplest, it just lets the user pick either to start the game or go into the settings. On a silly note, the movement of the letters can be changed in the configs file

## Settings
--------
The settings menu lets the player tweak world paramters, screen parameters and turn on and off optional stuff. It basically functions as a way to edit the game configs on the fly, without hard coding anything. There are 4 tabs in the Settings menu, and the current tab and chosen option is shown by glowing orange (for the tabs) and yellow (for the options). Here is a breakdown of all the options organized by tabs


### General:
The general tab has screen related stuff, and only has 2 options those being 
- Resolution: Lets the user change the current screen size. Including letting them input a custom height and width, cannot set either to 0, then the game crashes.
- Fullscreen: If True then the game enters fullscreen mode. If you're in full screen mode, it still uses the set resolution but fills out your entire screen as that. This means you can use it to set
  A makeshift zoom level to the game by setting the resolution to something like 4k x 2k
Note: FPS was considered to be put here as well, but it got messy so it was left out. If the user really wants to change it they can do so in the configs file.

### Physics: 
The physics tab covers everything physics related (shocker). They all are floats, but plugging in intigers into the custom input works fine. Here is what all of them do
- Gravity:         Controls the global gravity strength constant G. It is normally set to 1, but can be changed to anything. Gets really messy with high values as ships get slignshot all over the screen
- Orbit Speed:     Controls how fast the planets orbit around the sun. This is also a multiplier, which is normally 1. Hihger numbers means faster spin around the sun.
- Planet Rotation: This is how fast the planets rotate around themselves. This is a multiplier which is normally 1, and changing this has no gameplay effect, just makes the planet sprites spin really fast.
- Friction:        The world base friction. This is a direct value not a multiplier. Class specific friction modifiers get added onto this value.
Note: Be careful when changing the friction. The cruiser class has negative friction, and as such setting the friction to 0 will give negative friction, meaning it never slows down, only speeds up.

### Ship:
The ship tab changes ship specific parameters (also shocker), these are all base cases, and class modifiers are added onto them. Everything here are intigers so the custom button will not let you input a float.
- Thrust Power:   Affects how fast the ship accelerates. Higher thrust means faster ship.
- Fuel Decay:     Affects how quickly fuel decays as a base level. Setting this to 0 means ships never run out of fuel.
- Bullet Speed:   Changes how fast the bullets shot by ships travel, of note: setting it to 0 does not mean they are stationary, as bullet speed is erlative to how quickly the player is moving when shooting.
- Starting Fuel:  Changes how much fuel the ships start with when spawning in, or when respawning. It is possible to set this above 100, but the fuel bar is not shown as going above 100 
- Rotation speed: Changes how fast ships rotate when pressing the left or right key.

### World:
Changes world related settings, everything here is an intiger, so cannot plug in floats.
- Number Of Barrels: Changes how many barrels spawn in when the main game is started up. WARNING, too many of these make the game run really poorly
- Fuel Per Barrel:   Changed how much fuel the player gets from collection fuel barrels, normally this is set to 20.
- Number Of Stars:   Changes how many stars are in the background, having too many of them makes the game run really poorly so be careful.
- Map Always On:     Makes the mini map no longer require the M key to show up on screen. It is smaller than normal but will not go away.

### Class
Changes character specific features and customization by changing the color of the ship, this also changes the color of the mini map icon.
The class system works as follows

Fighter: 
FIghter is the base 0, 0, 0 case, it does not improve or change anything and has no features. Its blast sprite is the longest but is also the thinnest. Bigger blasts are easier to hit with since their hitbox is larger.
This class is the basic one that's chosen by default. 

Cruiser:
This is supposed to be the speed class. It has higher speed, higher turn rate, quicker bullet cooldown and lower friction, but the bullets are really small so it's hard to hit things. It is also fairly hard to control this ship. The fuel decay is also higher on this stip.

Destroyer:
This is supposed to be the tank class. It is much slower than the other classes, the bullet rechange is high, the turn rate is slow and the thrust speed is low. To compensate for this the bullet sprite is larger than the other ships, the fuel decay is lower than the others and there is a mechanic where you can be hit 3 times before it counts as a death. This "shield" only works for bullets, it will not save you from crashing into the sun or something like that.

For each of the classes there are 4 color options, all made by me. There were plans to make a custom color option by drawing a transparent mask over the sprite to hue shift the ship sprites, but this did not look good so it was not done. 

All class modifiers can be changed in the configs file, and one can even add more classes if they want, linking up stuff from the configs file to the settings screen is fairly easy.


## MainGame
--------

### UI:
This is where the game runs, it does all of the logic and control handling. p1 controls the ship on the left side while p2 controls the one on the right. The player name can be seen at the top of the UI.
At the top of the UI one can also find the players score. 

- Hitting a player gives you 200 points
- Hitting a fuel barrel gives you 50 points
- Dying in any way removes 100 points.

If the points go negative the text goes red, so show you're in the negative.

At the top of the UI right before the camera, is the current world coordinates. The word map is 10,000 x 10,000, and so using the coordinates might not be too useful, but they turn red when the player hits a world border, which is quite nice as it's invisible.

At the bottom of the UI is the fuel bar, this can be clicked to add more fuel. The color of the fuel bar changed depending on how much fuel you have left:
- Green: If it's over 65% it's green
- Yellow: If it's less than 65% but over 45% it's yellow
- Orange: If it's less than 45% but over 20% it's orange
- Red: If it's less than 20% it's red


### Planets:

There are 7 celestial bodies in the game, all their properties are taken from the game Outer Wilds. The correct mass and orbital radius was found in the following spreadhsheet: https://docs.google.com/spreadsheets/d/1MbGYmH20m5NLCEsCe-v_kkn3oldxVY67vj4bF5UJMko/edit?gid=0\#gid=0

There are 5 different kinds of planets, each of them, and what planets fit into each type can be listed in the following way

Hazards: These celestial bodies kill you on collision, no matter what speed you travel at, there are 2 dangerous celestial bodies, those are
- Sun: The sun does not orbit anything, and is locked at the center of the world map. Going into the sun kills the player instantly.
- Dark Bramble: Dark Bramle is the second furhest out in the solar system, going into it will kill the player instantly for spoiler related reasons. Dark bramble does not rotate at all, which is source accurate. It is also not a planet, and neither is the sun, which is why I use wording like "celestial bodies" instead of just saying planets.

Safe zones: These planets let you land on them, if you go under the speed limit of 500 distance units per tick. If you surpass this speed and try to land, you'll die like on a hazard celestial body. There are 2 planets that let you land on them, and once you do you start to refuel. Those planets are the following
- Timber Hearth: This is the earth looking planet which is second closest to the sun. The moon (Attlerock) does not have a hitbox, as this would require more complex hitbox logic.
- Giants Deep: This is planet number 4 from the sun, it is a gas giant, and is landable. There should have been more mechanics tied to this planet, for lore reasons, but it got complicated so it's just a landable planet.

Bump: There is one planet that players can only bump into, or well technically two but they function as one planet. 
- Hourglass Twins: These two planets orbit eachother and is the planet(s) closest to the sun. Because they are so small, and have such a weird orbit, I decided not to add landing to them, and instead just treat them as something bumping into the player. This just pushes the player back, almost like when bumping into another player. Just like landable planets if you go too fast when collliding with the twins, you will die. The hitbox is set between the two planets, but it works fine enough.

White Hole: A White hole has negative mass, so it has reverse gravity, meaning it pushes everything away from it. There is one white hole in the solar system.
- White Hole Station: The white hole station is the object orbiting the furthest out from the sun. It pushes everything away from it. It also has no collision, so you cannot die from running ito it. But also, because the gravity is so strong, reaching the center is really difficult. 

Teleport: There is one planet that when collided with teleports the player to the white hole station at the edge of the worldmap.
- Brittle Hollow: Brittle Hollow is the third planet from the sun, and it does not have any collision. Instead, if you reach the center of the planet you reach a black hole that teleports you to the white hole at the outskirts of the solar system. Because it has no collision the player can enter Brittle Hollow as quickly as they want without worrying about crashing.

Given more time there would have been 3 more celestial bodies. 2 of them I cannot talk about for spoiler reasons, but one of them was supposed to be a comet (The interloper) that followed an eliptical curve. This was tricky to implement, and have it not hit other planets and such, so I just did not do it. The sun was also going to have some extra mechanics tied to it, but I ended up not adding it, for again spoiler reasons.
