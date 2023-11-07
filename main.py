from designer import *
from boulder import Boulder


class World:
    boulders: [Boulder]
    score: float
    
    def __init__(self):
        """
        Constructor for World.  Initialises the world with no boulders and a
            score of 0.
        """
        self.boulders = []
        self.score = 0.
    
    def move_boulders_down(self):
        """
        Loops through all of the boulders and moves them down.
        """
        for boulder in self.boulders:
            boulder.move_down()


def void_draw(world: World):
    """
    I'm using a name analogous to that used by Processing, as I find it easier
        to think about having a single function run on 'updating'.  I am likely
        to make similar functions for void_setup, void_keyPressed, etc.
    This function is just a handler for all of the things that need to happen
        each frame.
    
    Args:
        world (World): The world for the game.  Will be used by some of the
            functions called by this one.
    """
    world.move_boulders_down()


def main():
    when('starting', World)
    when('typing', Boulder)
    when('updating', void_draw)
    start()


if __name__ == "__main__":
    main()
