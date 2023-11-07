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


def main():
    when('starting', World)
    when('typing', Boulder)
    start()


if __name__ == "__main__":
    main()
