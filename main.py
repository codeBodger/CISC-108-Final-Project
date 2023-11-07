from designer import *
from boulder import Boulder
from useful_funcs import pm_bool


GUTTER = 200


class World:
    boulders: dict[int, Boulder]
    score: float = 0.
    text_score: DesignerObject
    selected: int = 0
    
    def __init__(self):
        """
        Constructor for World.  Initialises the world with no boulders and a
            score of 0.
        """
        self.boulders = {}
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
    
    def select(self, right: bool):
        """
        Selects the next boulder to the right if `right` is True, or to the left
            if `right` is False (ignoring those above the window).

        Args:
            right (bool): Whether to select the next to the right or to the left
        """
        new_selected_index = 0
        sorted_keys = sorted(list(self.boulders.keys()))
        for i, key in enumerate(sorted_keys):
            self.boulders[key].boulder.alpha = .5
            if key == self.selected:
                new_selected_index = i + pm_bool(right)
                new_selected_index = new_selected_index % len(self.boulders)
        self.selected = sorted_keys[new_selected_index]
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
        case _:
            print(key)


def main():
    when('starting', void_setup)
    when('updating', void_draw)
    when('typing', void_keyPressed)
    start()


if __name__ == "__main__":
    main()
