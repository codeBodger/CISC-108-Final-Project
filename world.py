from designer import *
from designer import __version__ as DESIGNER_VERSION
from random import random as rand
from boulder import Boulder
from useful import pm_bool, int_from_pattern, ensure_version, MatchStr, MatchIter
from scale import ScaleInfo


MIN_DESIGNER_VERSION = "0.6.3"

GUTTER = 200  # How far away from the right to put the score and other info
FAILED_BOULDER_PENALTY = -5

BOULDER_MAX_PROB = 2 ** -6
MAX_BOULDERS = 4

# A dictionary to store some info about the types of scale, indexed with the
# key that must be pressed to choose the type of scale
SCALE_TYPE_INFO = {
    "q": ScaleInfo("Major",          "WWHWWWH", [
        "Cb4", "Gb4", "Db4", "Ab4", "Eb4", "Bb4", "F4",
        "C4", "G4", "D4", "A4", "E4", "B4", "F#4", "C#4"
    ]),
    "w": ScaleInfo("Natural Minor",  "WHWWHWW", [
        "Ab4", "Eb4", "Bb4", "F4", "C4", "G4", "D4",
        "A4", "E4", "B4", "F#4", "C#4", "G#4", "D#4", "A#4"
    ]),
    "e": ScaleInfo("Harmonic Minor", "WHWWH3H", [
        "Ab4", "Eb4", "Bb4", "F4", "C4", "G4", "D4",
        "A4", "E4", "B4", "F#4", "C#4", "G#4", "D#4", "A#4"
    ]),
    "r": ScaleInfo("Melodic Minor",  "WHWWWWH", [
        "Ab4", "Eb4", "Bb4", "F4", "C4", "G4", "D4",
        "A4", "E4", "B4", "F#4", "C#4", "G#4", "D#4", "A#4"
    ])
}
SCALE_KEYS = MatchIter(SCALE_TYPE_INFO)


class World:
    boulders: dict[int, Boulder] = {}
    score: float = 0.
    text_score: DesignerObject
    scale_keys_text: [DesignerObject]
    selected: int = 0  # The key of the selected boulder, its x-coordinate
    paused: bool = False
    
    def __init__(self):
        """
        Constructor for World.  Initialises the world with no boulders and a
            score of 0.
        """
        self.text_score = text('black', f"{self.score:.4}", 30,
                               get_width(), 20,
                               font_name="Game Font", font_path="Game Font.ttf")
        scale_keys_strs = [
            f"{key}: {scale_type.name}"
            for key, scale_type in SCALE_TYPE_INFO.items()
        ]
        self.scale_keys_text = []
        for i, scale_keys_str in enumerate(scale_keys_strs):
            self.scale_keys_text.append(
                text('black', scale_keys_str, 20,
                     get_width() - GUTTER, 80 + 40*i, anchor="midleft",
                     font_name="Times New Roman")
            )

    def move_boulders_down(self):
        """
        Loops through all of the boulders and moves them down.
        """
        for boulder in self.boulders.values():
            boulder.move_down(self)
    
    def display_score(self):
        """
        Displays the score off to the side of the screen.  Run each frame
        """
        self.text_score.text = f"{self.score:.4}"
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
    
    def pause(self):
        """
        Pauses the game; i.e. hides the scales, stops the boulders, and prevents
            directly game-related input.
        """
        for boulder in self.boulders.values():
            set_visible(boulder.scale.display, self.paused)
            set_visible(boulder.scale.blur, not self.paused)
        self.paused = not self.paused
    

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
    world._ = Boulder(world)  # So it's actually displayed, the GC is too good.
    return world


def void_draw(world: World):
    """
    This function is just a handler for all of the things that need to happen
        each frame.
    
    Args:
        world (World): The world for the game.  Will be used by some of the
            functions called by this one.
    """
    if world.paused:
        return
    boulder_prob = .1 + .9 / (1 + 2.7**( 2 - world.score/25) )
    boulder_prob *= BOULDER_MAX_PROB
    if len(world.boulders) == 0:
        boulder_prob = BOULDER_MAX_PROB
    if rand() < boulder_prob and len(world.boulders) < MAX_BOULDERS:
        print(boulder_prob)
        Boulder(world)
    world.move_boulders_down()
    world.remove_fallen_boulders()
    world.display_score()


def void_keyPressed(world: World, key: str):
    """
    This function is just a handler for all of the things that need to happen on
        keypress.  It also handles the different things that need to happen when
        different keys are pressed.
    Note: this function name is partially in camelCase because I'm using a name
        analogous to that used for the purpose in Processing.
    
    Args:
        world (World): The world for the game.  Well be used by some of the
            functions called by this one.
        key (str): The key that was pressed.
    """
    match MatchStr(str(key)):
        # if not world.paused:
        case 'left' if not world.paused:
            world.select_previous()
        case 'right' if not world.paused:
            world.select_next()
        case SCALE_KEYS.value if not world.paused:
            if world.selected == 0:
                return
            selected_boulder = world.boulders[world.selected]
            sb_pattern = selected_boulder.scale.pattern
            guessed_pattern_str = SCALE_TYPE_INFO[key].pattern
            guessed_pattern = [int_from_pattern(c) for c in guessed_pattern_str]
            if sb_pattern == guessed_pattern:
                world.score += selected_boulder.value
                selected_boulder.remove(world)
            else:
                selected_boulder.value *= 0.50
        # Either way
        case 'escape':
            exit(world.score)
        case 'space':
            world.pause()
        case _:
            print(key)


def main():
    if not ensure_version(DESIGNER_VERSION, MIN_DESIGNER_VERSION):
        raise Exception(
            f"DesignerVersionError: {DESIGNER_VERSION}, "
            f"Version {MIN_DESIGNER_VERSION} or higher is required."
        )
    
    when('starting', void_setup)
    when('updating', void_draw)
    when('typing', void_keyPressed)
    start()


if __name__ == "__main__":
    main()
