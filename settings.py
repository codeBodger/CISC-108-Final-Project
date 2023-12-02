import json
from designer import *
from dataclasses import dataclass, asdict, field
from useful import Menu, MenuEntry, GAME_FONT_PATH, pm_bool, GAME_FONT_NAME
from scale import TOTAL_NOTES, LEDGER_LINES, NOTES_START


DEFAULT_CONFIG = {
    "scale_types": ["Major", "Natural Minor", "Harmonic Minor", "Melodic Minor"],
    "clefs": ["Treble", "Bass"],
    "max_sharps_key_signature": 4,
    "max_flats_key_signature": 4,
    "max_high_ledger_positions": 4,
    "max_low_ledger_positions": 4,
}


@dataclass(kw_only=True)
class Settings(object):
    scale_types: [str]
    clefs: [str]
    max_sharps_key_signature: int
    max_flats_key_signature: int
    max_high_ledger_positions: int
    max_low_ledger_positions: int
    
    @classmethod
    def load(cls):
        try:
            with open(".config.json") as f:
                config_string = f.read()
                config = json.loads(config_string)
        except FileNotFoundError:
            config = DEFAULT_CONFIG
        
        self = super().__new__(cls)
        self.__init__(**config)
        return self
    
    def save(self):
        config = asdict(self)
        config_string = json.dumps(config, indent=2)
        with open(".config.json", "w") as f:
            f.write(config_string)


@dataclass
class SettingsScreen(Menu):
    settings: Settings = field(default_factory=Settings.load)
    active_sub_menu: str = None
    active_sub_menu_left: bool = True
    sub_menu: [DesignerObject] = None


def ledger_lines(menu: SettingsScreen, update: bool = False):
    menu.settings.max_low_ledger_positions = min(
        menu.settings.max_low_ledger_positions, LEDGER_LINES
    )
    menu.settings.max_high_ledger_positions = min(
        menu.settings.max_high_ledger_positions, LEDGER_LINES
    )
    menu.settings.max_low_ledger_positions = max(
        menu.settings.max_low_ledger_positions, 0
    )
    menu.settings.max_high_ledger_positions = max(
        menu.settings.max_high_ledger_positions, 0
    )
    
    low_ledger_line  = chr(NOTES_START + LEDGER_LINES + 1
                           - menu.settings.max_low_ledger_positions)
    high_ledger_line = chr(NOTES_START + TOTAL_NOTES - LEDGER_LINES
                           + menu.settings.max_high_ledger_positions)
    
    if update:
        menu.sub_menu[0].text = low_ledger_line
        menu.sub_menu[0].alpha = 1. if menu.active_sub_menu_left else .3
        menu.sub_menu[1].text = high_ledger_line
        menu.sub_menu[1].alpha = .3 if menu.active_sub_menu_left else 1.
    else:
        menu.active_sub_menu = "ledger lines"
        menu.active_sub_menu_left = True
        menu.sub_menu = [
            text('black', low_ledger_line, 60, anchor="midright",
                 font_name=GAME_FONT_NAME, font_path=GAME_FONT_PATH),
            text('black', high_ledger_line, 60, anchor="midleft",
                 font_name=GAME_FONT_NAME, font_path=GAME_FONT_PATH, alpha=.3)
        ]
        menu.sub_menu[0].x -= 30
        menu.sub_menu[1].x += 30


HEADER = "Settings: Press a number key to continue"
ENTRIES = [
    MenuEntry("Enable/Disable Standard Scales", print, "Standard Scales"),
    MenuEntry("Enable/Disable Church Modes", print, "Church Modes"),
    MenuEntry("Enable/Disable Clefs", print, "Clefs"),
    MenuEntry("Increase/Decrease Key Signature Range", print, "Keys"),
    MenuEntry("Increase/Decrease Ledger Lines", ledger_lines)
]


def exit_sub_menu(menu: SettingsScreen):
    menu.active_sub_menu = None
    menu.active_sub_menu_left = True
    for designer_object in menu.sub_menu:
        destroy(designer_object)
    menu.sub_menu = None


def void_setup():
    return SettingsScreen(HEADER, ENTRIES,
                          left=True, size_percent=70, margin_left=20)


def void_keyPressed(menu: SettingsScreen, key: str):
    match menu.active_sub_menu:
        case "ledger lines":
            change = 0
            match key:
                case 'left' | 'right':
                    menu.active_sub_menu_left ^= True  # not
                case 'up' | 'down':
                    change = pm_bool(key == 'down')
                case 'escape':
                    exit_sub_menu(menu)
                    return
            if menu.active_sub_menu_left:
                menu.settings.max_low_ledger_positions  += change
            else:
                menu.settings.max_high_ledger_positions -= change
            ledger_lines(menu, update=True)
        case _:
            if not menu.select(key, menu):
                match key:
                    case "escape":
                        menu.settings.save()
                        pop_scene()
                    case _:
                        print(key)


def whens():
    """
    Calls all of the required `when`s for the settings menu.
    """
    when('starting: settings_menu', void_setup)
    when('typing: settings_menu', void_keyPressed)
