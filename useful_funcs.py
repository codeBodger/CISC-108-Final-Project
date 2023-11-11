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


def int_from_pattern(pattern_char: str) -> int:
    """
    Takes in a char from a scale pattern and returns an integer that's more
        useful.
        
    Args:
        pattern_char (str): The single character to convert

    Returns:
        int: The converted value
    """
    match pattern_char:
        case 'H':
            return 1
        case 'W':
            return 2
        case '3':
            return 3
        case _:
            return 0
    
    
def ensure_octave(pattern: [int]) -> bool:
    """
    Ensures that the input scale pattern fits exactly in an octave.
    
    Args:
        pattern (list[int]): The scale pattern to evaluate.

    Returns:
        bool: Whether or not it's a valid scale.
    """
    return sum(pattern) == 12


def get_next_letter(letter: str) -> str:
    """
    Gets the next letter in the musical alphabet.
    
    Args:
        letter (str): The letter to increase from.

    Returns:
        str: The next letter.
    """
    num = ord(letter) - ord('A') + 1
    num = num % 7
    return chr(num + ord('A'))


# Allows the program to be run starting in this file, in addition to main.py
if __name__ == "__main__":
    # from main import main
    # main()
    print(get_next_letter('G'))
    