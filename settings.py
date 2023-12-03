import json
from designer import *
from dataclasses import dataclass, asdict, field
from useful import Menu, MenuEntry, GAME_FONT_PATH, pm_bool, GAME_FONT_NAME
from scale import TOTAL_NOTES, LEDGER_LINES, NOTES_START, LETTERS_PER_OCTAVE


DEFAULT_CONFIG = {
    "scale_types": ["Major",
                    "Natural Minor", "Harmonic Minor", "Melodic Minor"],
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
    
    def __post_init__(self):
        self.validate()
    
    @classmethod
    def load(cls):
        try:
            with open(".config.json") as f:
                config_string = f.read()
                config = json.loads(config_string)
        except FileNotFoundError:
            config = DEFAULT_CONFIG
        
        self = Settings(**config)
        return self
    
    def save(self):
        config = asdict(self)
        config_string = json.dumps(config, indent=2)
        with open(".config.json", "w") as f:
            f.write(config_string)
    
    def validate(self):
        self.validate_key_signatures()
        self.validate_ledger_lines()
        
    def validate_key_signatures(self):
        self.max_sharps_key_signature = min(
            self.max_sharps_key_signature, LETTERS_PER_OCTAVE
        )
        self.max_flats_key_signature = min(
            self.max_flats_key_signature, LETTERS_PER_OCTAVE
        )
        self.max_sharps_key_signature = max(
            self.max_sharps_key_signature, 0
        )
        self.max_flats_key_signature = max(
            self.max_flats_key_signature, 0
        )
    
    def validate_ledger_lines(self):
        self.max_low_ledger_positions = min(
            self.max_low_ledger_positions, LEDGER_LINES
        )
        self.max_high_ledger_positions = min(
            self.max_high_ledger_positions, LEDGER_LINES
        )
        self.max_low_ledger_positions = max(
            self.max_low_ledger_positions, 0
        )
        self.max_high_ledger_positions = max(
            self.max_high_ledger_positions, 0
        )


@dataclass
class SettingsScreen(Menu):
    header: str = "Settings: Press a number key to continue"
    entries: [MenuEntry] = None
    settings: Settings = field(default_factory=Settings.load)
    active_sub_menu: str = ""
    active_sub_menu_left: bool = True
    sub_menu: [DesignerObject] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.entries = [
            MenuEntry("Enable/Disable Standard Scales", print, "Standard Scales"),
            MenuEntry("Enable/Disable Church Modes", print, "Church Modes"),
            MenuEntry("Enable/Disable Clefs", print, "Clefs"),
            MenuEntry("Increase/Decrease Key Signature Range", print, "Keys"),
            MenuEntry("Increase/Decrease Ledger Lines", self.ledger_lines)
        ]

    def ledger_lines(self):
        self.settings.validate_ledger_lines()
        
        low_ledger_line  = chr(NOTES_START + LEDGER_LINES + 1
                               - self.settings.max_low_ledger_positions)
        high_ledger_line = chr(NOTES_START + TOTAL_NOTES - LEDGER_LINES
                               + self.settings.max_high_ledger_positions)
        
        if self.active_sub_menu == "ledger lines":
            self.sub_menu[0].text = low_ledger_line
            self.sub_menu[0].alpha = 1. if self.active_sub_menu_left else .3
            self.sub_menu[1].text = high_ledger_line
        else:
            self.sub_menu[1].alpha = .3 if self.active_sub_menu_left else 1.
            self.active_sub_menu = "ledger lines"
            self.active_sub_menu_left = True
            self.sub_menu = [
                text('black', low_ledger_line, 60, anchor="midright",
                     font_name=GAME_FONT_NAME, font_path=GAME_FONT_PATH),
                text('black', high_ledger_line, 60, anchor="midleft",
                     font_name=GAME_FONT_NAME, font_path=GAME_FONT_PATH, alpha=.3)
            ]
            self.sub_menu[0].x -= 30
            self.sub_menu[1].x += 30

    def exit_sub_menu(self):
        self.active_sub_menu = ""
        self.active_sub_menu_left = True
        for designer_object in self.sub_menu:
            destroy(designer_object)
        self.sub_menu = None


def void_setup():
    return SettingsScreen(left=True, size_percent=70, margin_left=20)


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
                    menu.exit_sub_menu()
                    return
            if menu.active_sub_menu_left:
                menu.settings.max_low_ledger_positions  += change
            else:
                menu.settings.max_high_ledger_positions -= change
            menu.ledger_lines()
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
