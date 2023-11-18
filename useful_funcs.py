from typing import Union
from collections.abc import Iterable
from dataclasses import dataclass


def pm_bool(b: bool) -> int:
    """
    Converts a boolean to +-1
    Returns `1` if b is True, `-1` if b is False
    
    Args:
        b (bool): The boolean to be converted

    Returns:
        int: Either 1 or -1, depending on b
    """
    return b * 2 - 1


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


def cmp(a, b) -> int:
    """
    Returns:
        int: 0 if a and b are the same, -1 if a < b, 1 if a > b
    """
    return (a > b) - (a < b)


def ensure_version(actual: str, required: str) -> bool:
    """
    Tests if the version of a program/module is high enough.
    
    Args:
        actual (str): The actual version that we're testing
        required (str): The minimum version that we're testing against

    Returns:
        bool: Whether or not the program/module is new enough
    """
    return (
            tuple(map(int, (actual.split("."))))
            >=
            tuple(map(int, (required.split("."))))
    )


def boulder_speed(score: float, base_speed: int) -> float:
    """
    Finds the speed with which to move the boulders down, given the player's
        current score.
    
    Args:
        score (int): The player's score
        base_speed (int): The base speed of the boulders, when the score is less
            than 1

    Returns:
        int: The speed for the boulders
    """
    if score < 1:
        return base_speed
    return base_speed * (1 + ((score - 1) / 30) ** .9)


@dataclass
class MatchIter:
    value: Iterable
    

class MatchStr(str):
    def __eq__(self, match_list: Union[Iterable, str]) -> bool:
        """
        Checks if the value of the MatchStr is in the list, or if it is equal to
            the string.
        
        Args:
            match_list (Iterable or str): The list or string to check against

        Returns:
            bool: Whether or not the value of the MatchStr is in the list or is
                equal to the string
        """
        if isinstance(match_list, str):
            return match_list.__eq__(self)
        else:
            return self in list(match_list)
