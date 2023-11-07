def pm_bool(b: bool) -> int:
    """
    Converts a boolean to +-1
    Returns `1` if b is True, `-1` if b is False
    
    Args:
        b (bool): The boolean to be converted

    Returns:
        int: Either 1 or -1, depending on b
    """
    return b*2 -1


# Allows the program to be run starting in this file, in addition to main.py
if __name__ == "__main__":
    from main import main
    main()
    