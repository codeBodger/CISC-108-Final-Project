from designer import *
from useful import Menu, MenuEntry


HEADER = "Settings: Press a number key to continue"
ENTRIES = [
    MenuEntry("temp_label", print, "settings!!")
]


def void_setup():
    return Menu(HEADER, ENTRIES)


def void_keyPressed(menu: Menu, key: str):
    if not menu.select(key):
        match key:
            case "escape":
                pop_scene()
            case _:
                print(key)


def whens():
    """
    Calls all of the required `when`s for the settings menu.
    """
    when('starting: settings_menu', void_setup)
    when('typing: settings_menu', void_keyPressed)
