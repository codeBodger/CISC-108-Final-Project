from designer import *
from random import random as rand
from dataclasses import dataclass, field
from boulder import Boulder
from settings import Settings
from useful import pm_bool, int_from_pattern, MatchStr, MatchIter, \
    GAME_FONT_PATH, GAME_FONT_NAME, make_scale_keys_text, GUTTER
from scale import SCALE_TYPE_INFO, SCALE_TYPE_KEYS

FAILED_BOULDER_PENALTY = -5

BOULDER_MAX_PROB = 2 ** -6
MAX_BOULDERS = 4

SCALE_KEYS = MatchIter(SCALE_TYPE_INFO)


@dataclass
class World:
    text_score: DesignerObject = None
    scale_keys_text: [DesignerObject] = None
    boulders: dict[int, Boulder] = field(default_factory=dict)
    score: float = 0.
    selected: int = 0  # The key of the selected boulder, its x-coordinate
    paused: bool = False
    settings: Settings = None
    
    def __post_init__(self):
        """
        Real constructor for World (__init__() really just calls this; I wanted
            to have the list of attrs at the top, but pointers made this
            impossible, so I had to use a dataclass, even when I wanted my own
            __init__().  This was the best that I could come up with).
            Initialises the world with no boulders and a score of 0.
        """
        self.settings = Settings.load()
        
        self.text_score = text(
            'black', f"{self.score:.4}", 30,
            get_width(), 20,
            font_name=GAME_FONT_NAME, font_path=GAME_FONT_PATH)
        scale_keys_set = set(SCALE_TYPE_KEYS) & set(self.settings.scale_types)
        self.scale_keys_text = make_scale_keys_text(scale_keys_set)
        
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
            print(world.score)
            pop_scene()
        case 'space':
            world.pause()
        case _:
            print(key)


def whens():
    """
    Calls all of the required `when`s for the main game.
    """
    when('starting: world', void_setup)
    when('updating: world', void_draw)
    when('typing: world', void_keyPressed)
