from designer import *
from boulder import Boulder
from useful_funcs import pm_bool


GUTTER = 200
FAILED_BOULDER_PENALTY = -10


class World:
    boulders: dict[int, Boulder] = {}
    score: float = 0.
    text_score: DesignerObject
    selected: int = 0  # The key of the selected boulder, its x-coordinate
    
    def __init__(self):
        """
        Constructor for World.  Initialises the world with no boulders and a
            score of 0.
        """
        self.text_score = text('black', f"Score: {self.score:.4}",
                               30, get_width(), 20)
    
    def move_boulders_down(self):
        """
        Loops through all of the boulders and moves them down.
        """
        for boulder in self.boulders.values():
            boulder.move_down()
    
    def display_score(self):
        """
        Displays the score off to the side of the screen.  Run each frame
        """
        self.text_score.text = f"Score: {self.score:.4}"
        self.text_score.x = get_width() - (GUTTER - self.text_score.width//2)
    
    def sorted_onscreen_boulder_keys(self) -> [int]:
        """
        Gets a sorted list of the keys of the boulders that are below the top of
            the game window.
        
        Returns:
            list[int]: A sorted list of useful boulder keys
        """
        keys = sorted(list(self.boulders.keys()))
        good_keys = []
        for key in keys:
            if self.boulders[key].boulder.y > 0:
                good_keys.append(key)
        return good_keys
    
    def key_of_max_y_boulder(self) -> int:
        """
        Gets the key of the boulder with the highest y-coordinate (lowest down
            in the window).
        
        Returns:
            int: The key of said boulder.
        """
        boulders = list(self.boulders.values())
        max_y = boulders[0]
        for boulder in boulders:
            if boulder.boulder.y > max_y.boulder.y:
                max_y = boulder
        return max_y.boulder.x
    
    def select(self, right: bool):
        """
        Selects the next boulder to the right if `right` is True, or to the left
            if `right` is False (ignoring those above the window).
        If all of the boulders are above the window, always select the lowest.
        If there are no boulders, select the non-existent boulder at 0.

        Args:
            right (bool): Whether to select the next to the right or to the left
        """
        if not self.boulders:
            self.selected = 0
            return
        
        good_sorted_keys = self.sorted_onscreen_boulder_keys()
        if not good_sorted_keys:
            self.selected = self.key_of_max_y_boulder()
            return
        
        if right:
            good_sorted_keys = list(reversed(good_sorted_keys))
        new_selected = good_sorted_keys[-1]
        for key in good_sorted_keys:
            self.boulders[key].boulder.alpha = .5
            if pm_bool(right)*key > self.selected*pm_bool(right):
                new_selected = key
        
        self.selected = new_selected
        self.boulders[self.selected].boulder.alpha = 1
    
    def select_previous(self):
        """
        Selects the next boulder to the left (ignoring those above the window).
        """
        self.select(False)
        
    def select_next(self):
        """
        Selects the next boulder to the right (ignoring those above the window).
        """
        self.select(True)
    
    def update_score(self, amount: float):
        """
        Updates the player's score.
        
        Args:
            amount (float): The amount to change the score by (can be + or -)
        """
        self.score += amount
    
    def remove_fallen_boulders(self):
        """
        Removes any boulders that have fallen below the bottom of the window and
            decreases the score by FAILED_BOULDER_PENALTY.
        """
        for boulder in list(self.boulders.values()):
            if boulder.boulder.y > get_height():
                boulder.remove(self)
                self.update_score(FAILED_BOULDER_PENALTY)


def void_setup() -> World:
    """
    I'm using a name analogous to that used by Processing, as I find it easier
        to think about having a single function run on 'starting'.  I have
        similar functions for void_draw and void_keyPressed
    This function is just a handler for all of the things that need to happen
        on startup.

    Returns:
        World: The world for the game, which will be passed to all other
            functions called from `when()`.  Will be used by some of the
            functions called by this one.
    """
    world = World()
    return world


def void_draw(world: World):
    """
    This function is just a handler for all of the things that need to happen
        each frame.
    
    Args:
        world (World): The world for the game.  Will be used by some of the
            functions called by this one.
    """
    world.move_boulders_down()
    world.remove_fallen_boulders()
    world.display_score()


def void_keyPressed(world: World, key: int):
    """
    This function is just a handler for all of the things that need to happen on
        keypress.  It also handles the different things that need to happen when
        different keys are pressed.
    
    Args:
        world (World): The world for the game.  Well be used by some of the
            functions called by this one.
        key (str): The key that was pressed.
    """
    match key:
        case 'space':
            Boulder(world)
        case 'left':
            world.select_previous()
        case 'right':
            world.select_next()
        case 'escape':
            exit(-1)
        case _:
            print(key)


def main():
    when('starting', void_setup)
    when('updating', void_draw)
    when('typing', void_keyPressed)
    start()


if __name__ == "__main__":
    main()
