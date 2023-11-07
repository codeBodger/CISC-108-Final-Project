# Imports for type checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Normal imports
from designer import *
from random import randint

if TYPE_CHECKING:
    from main import World


BOULDER_SCALE = 5
BOULDER_WIDTH = BOULDER_SCALE * 34
BOULDER_SPEED = 2


class Boulder:
    # scale: Scale
    boulder: DesignerObject
    
    def __init__(self, world: World):
        """
        Constructor for Boulder.  Creates a boulder randomly across the top of
            the screen, ensuring that it does not hang off of the left-right
            edge.  If the boulder overlaps with another boulder, move it up
            until it doesn't.  If it's too far above of the window, remove it
            and don't add it to the world.
        
        Args:
            world (World): The world in which the boulder is created.  Is used
                to ensure that boulders don't overlap, and for the boulders to
                be added to.
        """
        self.boulder = emoji(
            "🪨",
            randint(BOULDER_WIDTH//2, get_width() - BOULDER_WIDTH//2),
            0
        )
        self.boulder.scale = BOULDER_SCALE
        while self.is_colliding_somewhere(world):
            self.shift_up()
        if self.boulder.y < -2 * self.boulder.height:
            self.boulder.destroy()
        else:
            world.boulders.append(self)
    
    def is_colliding_somewhere(self, world: World) -> bool:
        """
        Checks if this boulder is colliding with any other boulders in the world.
        
        Args:
            world (World): The world in which to check the boulders.

        Returns:
            bool: Whether or not this boulder is colliding.
        """
        for boulder in world.boulders:
            if colliding(self.boulder, boulder.boulder):
                return True
        return False
    
    def shift_up(self):
        """
        Moves the boulder up by half of the height of the boulder, ideally so
            it is no longer overlapping any other boulders.
        """
        self.boulder.y -= self.boulder.height//2
    
    def move_down(self):
        """
        Moves the boulder down by BOULDER_SPEED.  This happens every frame.
        """
        self.boulder.y += BOULDER_SPEED


# Allows the program to be run starting in this file, in addition to main.py
if __name__ == "__main__":
    from main import main
    main()
