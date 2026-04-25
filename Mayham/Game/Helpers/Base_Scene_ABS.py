"""Abstract scene contract used by all screens"""

from abc import ABC, abstractmethod


class BaseScene(ABC):
    """Parent class for scenes rendered by the main loop, taken from Pokemon code"""

    def __init__(self, screen : object):
        """Store pygame screen and cached dimensions"""
        self.screen        = screen
        self.screen_width  = screen.get_width()
        self.screen_height = screen.get_height()
        self.font          = "Assets/pokemon_font.ttf"
        self.orange        = (233, 119, 57) 

    @abstractmethod
    def handle_events(self, events : object):
        """Process input events and optionally return the next scene"""

    @abstractmethod
    def update(self, dt : float):
        """Update scene state for a single frame"""

    @abstractmethod
    def draw(self) -> None:
        """Render the scene to the screen surface"""