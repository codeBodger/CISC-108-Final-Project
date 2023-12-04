from designer import *
from designer import __version__ as DESIGNER_VERSION
from useful import ensure_version, Menu, MenuEntry

MIN_DESIGNER_VERSION = "0.6.3"

HEADER = "Main Menu: Press a number key to continue"
ENTRIES = [
    MenuEntry("Play", push_scene, "world"),
    MenuEntry("Settings", push_scene, "settings_menu")
]


def void_setup():
    """ See world.void_setup for explanation """
    return Menu(HEADER, ENTRIES)


def void_keyPressed(menu: Menu, key: str):
    """ See world.void_keyPressed for explanation """
    if not menu.select(key):
        match key:
            case "escape":
                stop()
            case _:
                print(key)


def main():
    """ Main handler for the entire program """
    if not ensure_version(DESIGNER_VERSION, MIN_DESIGNER_VERSION):
        raise Exception(
            f"DesignerVersionError: {DESIGNER_VERSION}, "
            f"Version {MIN_DESIGNER_VERSION} or higher is required."
        )
    
    when('starting: main_menu', void_setup)
    when('typing: main_menu', void_keyPressed)
    import world
    world.whens()
    import settings
    settings.whens()
    start()


if __name__ == "__main__":
    main()
