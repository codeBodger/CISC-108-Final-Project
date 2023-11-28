from designer import *
from designer import __version__ as DESIGNER_VERSION
from useful import ensure_version, Menu, MenuEntry


MIN_DESIGNER_VERSION = "0.6.3"


class MainMenu:
    menu_structure: Menu = Menu(
        "Press a number key to continue",
        [
            MenuEntry("Play", push_scene, "world"),
            MenuEntry("Settings", push_scene, "settings_menu")
        ]
    )
    menu_label: DesignerObject
    menu_text: [DesignerObject]
    
    def __init__(self):
        self.menu_label = text(
            "black", self.menu_structure.header, 40,
            get_width()/2, 40
        )
        
        self.menu_text = []
        for i, menu_entry in enumerate(self.menu_structure.entries):
            self.menu_text.append(text(
                "black", f"{i+1}. {menu_entry.label}", 30,
                get_width()/2, 100 + 50*i
            ))


def void_setup():
    return MainMenu()


def void_keyPressed(menu: MainMenu, key: str):
    try:
        choice = (int(
            str(key)
            .replace("[", "")
            .replace("]", ""))
                  - 1)
        if choice < 0:
            raise IndexError("Negatives are out of bounds here.")
        menu.menu_structure.entries[choice]()
    except (ValueError, IndexError):
        print(key)


def main():
    if not ensure_version(DESIGNER_VERSION, MIN_DESIGNER_VERSION):
        raise Exception(
            f"DesignerVersionError: {DESIGNER_VERSION}, "
            f"Version {MIN_DESIGNER_VERSION} or higher is required."
        )
    
    when('starting: main_menu', void_setup)
    when('typing: main_menu', void_keyPressed)
    import world
    world.whens()
    start()


if __name__ == "__main__":
    main()
