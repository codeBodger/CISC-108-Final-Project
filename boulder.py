# Imports for type checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Normal imports
from designer import *
from random import randint
from scale import Scale
from useful import boulder_speed

if TYPE_CHECKING:
    from world import World


BOULDER_SCALE = 5
BOULDER_WIDTH = BOULDER_SCALE * 34
BOULDER_BASE_SPEED = 1
BOULDER_SPEED = 2
BOULDER_BASE_POINTS = 1


class Boulder:
    scale: Scale
    boulder: DesignerObject
    value: float = BOULDER_BASE_POINTS
    
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
        from world import GUTTER
        x = randint(BOULDER_WIDTH//2, get_width() - BOULDER_WIDTH//2 - GUTTER)
        y = 0
        
        self.boulder = emoji("🪨", x, y)
        self.boulder.scale = BOULDER_SCALE
        while self.is_colliding_somewhere(world):
            self.shift_up()
        if self.boulder.y < -2 * self.boulder.height:
            self.boulder.destroy()
        else:
            self.boulder.alpha = .5
            world.boulders[self.boulder.x] = self
            if len(world.boulders) == 1:
                world.selected = self.boulder.x
                self.boulder.alpha = 1
    
        self.scale = Scale(world)
        self.scale.make_text(self.boulder.x, self.boulder.y)
    
    def is_colliding_somewhere(self, world: World) -> bool:
        """
        Checks if this boulder is colliding with any other boulders in the world.
        Or if the boulder has the same x-coordinate as another boulder.
        
        Args:
            world (World): The world in which to check the boulders.

        Returns:
            bool: Whether this boulder is colliding or otherwise interfering
                with an existing boulder.
        """
        for boulder in world.boulders.values():
            if colliding(self.boulder, boulder.boulder):
                return True
            if self.boulder.x == boulder.boulder.x:
                return True
        return False
    
    def shift_up(self):
        """
        Moves the boulder up by half of the height of the boulder, ideally so
            it is no longer overlapping any other boulders.
        """
        self.boulder.y -= self.boulder.height//2
    
    def remove(self, world: World):
        """
        Removes this boulder from the game and from the dictionary of boulders.
        If this boulder was selected, select the next one.
        """
        self.scale.remove()
        x = self.boulder.x
        del world.boulders[self.boulder.x]
        destroy(self.boulder)
        if x == world.selected:
            world.select_lowest()

    def move_down(self, world: World):
        """
        Moves the boulder down by BOULDER_SPEED.  This happens every frame.
        """
        speed = boulder_speed(world.score, BOULDER_BASE_SPEED)
        self.boulder.y += speed
        self.scale.move_down(speed)
