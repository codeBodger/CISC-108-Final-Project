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


class Boulder:
    # scale: Scale
    boulder: DesignerObject
    
    def __init__(self, world: World):
        """
        Constructor for Boulder.  Creates a boulder randomly across the top of
            the screen.
        
        Args:
            world (World): The world in which the boulder is created.  Will be
                used to ensure boulders don't overlap.
        """
        self.boulder = emoji("🪨", randint(0, get_width()), 0)
        self.boulder.scale = BOULDER_SCALE


# Allows the program to be run starting in this file, in addition to main.py
if __name__ == "__main__":
    from main import main
    main()
