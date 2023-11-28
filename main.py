from designer import *
from designer import __version__ as DESIGNER_VERSION
from useful import ensure_version


MIN_DESIGNER_VERSION = "0.6.3"


class MainMenu:
    def __init__(self):
        pass


def void_setup():
    return MainMenu()


def void_keyPressed(menu: MainMenu, key: str):
    push_scene('world')


def main():
    if not ensure_version(DESIGNER_VERSION, MIN_DESIGNER_VERSION):
        raise Exception(
            f"DesignerVersionError: {DESIGNER_VERSION}, "
            f"Version {MIN_DESIGNER_VERSION} or higher is required."
        )
    
    when('starting: main_menu', void_setup)
    when('typing: main_menu', void_keyPressed)
    import world
    world.main()
    start()


if __name__ == "__main__":
    main()
