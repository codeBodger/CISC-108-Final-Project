import json
from designer import *
from dataclasses import dataclass, asdict, field
from useful import Menu, MenuEntry, GAME_FONT_PATH, pm_bool, GAME_FONT_NAME, \
    make_scale_keys_text, TEXT_FONT_NAME, ignore_numpad
from scale import TOTAL_NOTES, LEDGER_LINES, NOTES_START, LETTERS_PER_OCTAVE, \
    NORMAL_SCALE_NAMES, SCALE_TYPE_INFO, NORMAL_SCALE_KEYS, \
    CHURCH_MODES_NAMES, CHURCH_MODES_KEYS, CLEFS, CLEF_SYMBOLS_NAMES

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
        """ Causes self.validate() to be called after initialisation """
        self.validate()
    
    @classmethod
    def load(cls):
        """
        Returns a Settings object from the settings stored in .config.json, or
            if the config isn't found, uses the default settings.
        """
        try:
            with open(".config.json") as f:
                config_string = f.read()
                config = json.loads(config_string)
        except FileNotFoundError:
            config = DEFAULT_CONFIG
        
        self = Settings(**config)
        return self
    
    def save(self):
        """ Saves this Settings object as JSON data to .config.json """
        config = asdict(self)
        config_string = json.dumps(config, indent=2)
        with open(".config.json", "w") as f:
            f.write(config_string)
    
    def validate(self):
        """
        Handles checking of incoming data from .config.json to ensure that it's
            viable.  Additionally, handles fixing this data.
        """
        self.validate_scale_types()
        self.validate_clefs()
        self.validate_key_signatures()
        self.validate_ledger_lines()
    
    def validate_scale_types(self):
        """
        Handles the validation of the scale types: uses the default if none are
            listed in .config.json
        """
        if not self.scale_types:
            self.scale_types = DEFAULT_CONFIG["scale_types"]
    
    def validate_clefs(self):
        """
        Handles the validation of the clefs: uses the default if none are listed
            in .config.json
        """
        if not self.clefs:
            self.clefs = DEFAULT_CONFIG["clefs"]
    
    def validate_key_signatures(self):
        """
        Handles the validation of the key signatures, though functionality
            needing them hasn't been implemented.
        """
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
        """
        Handles the validation of the ledger lines: uses the closest viable
            count if the values stored in .config.json are out of range.
        """
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


ACTIVE   = 1.
INACTIVE = .3


@dataclass
class SettingsScreen(Menu):
    header: str = "Settings: Press a number key to continue or "\
                  "Esc to exit the menu or submenu"
    entries: [MenuEntry] = field(default_factory=list)
    settings: Settings = field(default_factory=Settings.load)
    active_sub_menu: str = ""
    active_sub_menu_left: bool = True
    sub_menu: list[Text] | Menu | None = None
    
    def __post_init__(self):
        """
        The SettingsScreen menu always has the same entries, so these are set in
            __post_init_(), after overriding the field and making it optional
        """
        self.entries = [
            MenuEntry("Enable/Disable Standard Scales", self.standard_scales),
            MenuEntry("Enable/Disable Church Modes", self.church_modes),
            MenuEntry("Enable/Disable Clefs", self.clefs),
            # MenuEntry("Increase/Decrease Key Signature Range", print, "Keys"),
            MenuEntry("Increase/Decrease Ledger Lines", self.ledger_lines)
        ]
        super().__post_init__()

    def standard_scales(self):
        """
        Handles the settings to enable and disable the standard scale types.
        """
        if self.active_sub_menu != "standard scales":
            self.active_sub_menu = "standard scales"
            self.sub_menu = [
                text('black', "Type a key to Enable/Disable a scale type", 24,
                     font_name=TEXT_FONT_NAME)
            ]
            self.sub_menu += make_scale_keys_text(NORMAL_SCALE_NAMES)
        for scale_type_text in self.sub_menu[1:]:
            if scale_type_text.text[3:] in self.settings.scale_types:
                scale_type_text.alpha = ACTIVE
            else:
                scale_type_text.alpha = INACTIVE
    
    def church_modes(self):
        """ Handles the settings to enable and disable the church modes. """
        if self.active_sub_menu != "church modes":
            self.active_sub_menu = "church modes"
            self.sub_menu = [
                text('black', "Type a key to Enable/Disable a scale type", 24,
                     font_name=TEXT_FONT_NAME)
            ]
            self.sub_menu += make_scale_keys_text(CHURCH_MODES_NAMES)
        for scale_type_text in self.sub_menu[1:]:
            if scale_type_text.text[3:] in self.settings.scale_types:
                scale_type_text.alpha = ACTIVE
            else:
                scale_type_text.alpha = INACTIVE

    def clefs(self):
        """ Handles the settings to enable and disable clefs. """
        if self.active_sub_menu != "clefs":
            self.active_sub_menu = "clefs"
            clef_entries = []
            for clef in CLEFS.values():
                clef_entry = MenuEntry(clef.symbol, self.toggle_clef, clef.name)
                clef_entries.append(clef_entry)
            self.sub_menu = Menu("Enable/Disable Clefs", clef_entries,
                                 left=True, margin_left=500, margin_top=50,
                                 body_font=(GAME_FONT_NAME, GAME_FONT_PATH))
        for text_ in self.sub_menu.menu_text:
            if CLEF_SYMBOLS_NAMES[text_.text[-1]] in self.settings.clefs:
                text_.alpha = ACTIVE
            else:
                text_.alpha = INACTIVE

    def toggle_clef(self, clef_name: str):
        """
        Special function to add or remove a clef from the list in the settings
        
        Args:
            clef_name (str): The name of the clef to enable or disable
        """
        if clef_name in self.settings.clefs:
            self.settings.clefs.remove(clef_name)
        else:
            self.settings.clefs.append(clef_name)
        self.clefs()

    def ledger_lines(self):
        """
        Handles changing the number of ledger lines, both at the top and bottom
            of the staff.
        """
        self.settings.validate_ledger_lines()
        
        low_ledger_line  = chr(NOTES_START + LEDGER_LINES + 1
                               - self.settings.max_low_ledger_positions)
        high_ledger_line = chr(NOTES_START + TOTAL_NOTES - LEDGER_LINES
                               + self.settings.max_high_ledger_positions)
        
        if self.active_sub_menu == "ledger lines":
            self.sub_menu[0].text = low_ledger_line
            self.sub_menu[0].alpha = (
                ACTIVE if self.active_sub_menu_left else INACTIVE
            )
            self.sub_menu[1].text = high_ledger_line
            self.sub_menu[1].alpha = (
                INACTIVE if self.active_sub_menu_left else ACTIVE
            )
        else:
            self.active_sub_menu = "ledger lines"
            self.active_sub_menu_left = True
            self.sub_menu = [
                text('black', low_ledger_line, 60, anchor="midright",
                     font_name=GAME_FONT_NAME, font_path=GAME_FONT_PATH),
                text('black', high_ledger_line, 60, anchor="midleft",
                     font_name=GAME_FONT_NAME, font_path=GAME_FONT_PATH,
                     alpha=INACTIVE)
            ]
            self.sub_menu[0].x -= 30
            self.sub_menu[1].x += 30

    def exit_sub_menu(self):
        """ Does everything needed to return to the main settings menu. """
        self.active_sub_menu = ""
        self.active_sub_menu_left = True
        if isinstance(self.sub_menu, Menu):
            self.sub_menu.destroy()
        if isinstance(self.sub_menu, list):
            for designer_object in self.sub_menu:
                destroy(designer_object)
        self.sub_menu = None


def void_setup():
    """ See world.void_setup for explanation """
    return SettingsScreen(left=True, size_percent=70, margin_left=20)


def void_keyPressed(menu: SettingsScreen, key: str):
    """ See world.void_keyPressed for explanation """
    key = ignore_numpad(key)
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
        case "standard scales" | "church modes":
            if key == 'escape':
                menu.exit_sub_menu()
            scale_keys, scale_names, scales = (
                (NORMAL_SCALE_KEYS, NORMAL_SCALE_NAMES, menu.standard_scales)
                if menu.active_sub_menu == "standard scales"
                else (CHURCH_MODES_KEYS, CHURCH_MODES_NAMES, menu.church_modes)
            )
            if key not in scale_keys:
                return
            scale_name = SCALE_TYPE_INFO[key].name
            if scale_name in scale_names:
                if scale_name in menu.settings.scale_types:
                    menu.settings.scale_types.remove(scale_name)
                else:
                    menu.settings.scale_types.append(scale_name)
            scales()
        case "clefs":
            if not menu.sub_menu.select(key):
                if key == "escape":
                    menu.exit_sub_menu()
        case _:
            if not menu.select(key):
                match key:
                    case "escape":
                        menu.settings.save()
                        pop_scene()
                    case _:
                        print(key)


def whens():
    """ Calls all of the required `when`s for the settings menu. """
    when('starting: settings_menu', void_setup)
    when('typing: settings_menu', void_keyPressed)
