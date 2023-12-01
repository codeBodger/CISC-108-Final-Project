import json
from designer import *
from dataclasses import dataclass, asdict, field
from useful import Menu, MenuEntry


DEFAULT_CONFIG = {
    "scale_types": ["Major", "Natural Minor", "Harmonic Minor", "Melodic Minor"],
    "clefs": ["Treble", "Bass"],
    "max_sharps_key_signature": 4,
    "max_flats_key_signature": 4,
    "max_high_ledger_positions": 4,
    "max_low_ledger_positions": 4,
}


HEADER = "Settings: Press a number key to continue"
ENTRIES = [
    MenuEntry("Enable/Disable Standard Scales", print, "Standard Scales"),
    MenuEntry("Enable/Disable Church Modes", print, "Church Modes"),
    MenuEntry("Enable/Disable Clefs", print, "Clefs"),
    MenuEntry("Increase/Decrease Key Signature Range", print, "Keys"),
    MenuEntry("Increase/Decrease Ledger Lines", print, "Ledger Lines"),
]


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
        print(cls)
        return self
    
    def save(self):
        config = asdict(self)
        config_string = json.dumps(config, indent=2)
        with open(".config.json", "w") as f:
            f.write(config_string)


@dataclass
class SettingsScreen(Menu):
    settings: Settings = field(default_factory=Settings.load)


def void_setup():
    return SettingsScreen(HEADER, ENTRIES,
                          left=True, size_percent=70, margin_left=20)


def void_keyPressed(menu: SettingsScreen, key: str):
    if not menu.select(key):
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
