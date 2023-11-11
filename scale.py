# Imports for type checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Normal imports
from designer import *
from useful_funcs import int_from_pattern, ensure_octave, get_next_letter, \
    pm_bool
from dataclasses import dataclass


# I might change these to better symbols at some point.
SHARP = '#'
FLAT  = 'b'

SCALE_TEXT_SIZE = 20


class Note:
    letter: str
    sharp_flat: str = ''
    octave: int
    
    def __init__(self, note: str):
        """
        Constructor for Note.  Creates a note from its string representation.
            Letters are just the first letter
            Octaves are found from the last digit of the string.
        
        Args:
            note (str): The string representation to be converted.
        """
        if ord('A') <= ord(note[0]) <= ord('G'):
            self.letter = note[0]
        else:
            raise Exception(f"InvalidNoteLetterError: {note[0]}")
        
        try:
            self.octave = int(note[-1])
        except ValueError:
            raise Exception(f"InvalidOctaveError: {note[-1]}")
        
        sharps_flats = 0
        for accidental in note[1:-1]:
            if accidental == '#':
                sharps_flats += 1
            elif accidental == 'b':
                sharps_flats -= 1
        self.sharp_flat = SHARP*sharps_flats + FLAT*-sharps_flats

    def __str__(self) -> str:
        """
        Automatically called when a Note is passed into print or str.  It will
            be very similar to what was passed in to the constructor.
        
        Returns:
            str: The string representation of the Note
        """
        return f"{self.letter}{self.sharp_flat} {self.octave}"
    
    def string_form(self, octave: bool = False) -> str:
        """
        Makes a string version of the note, very similar to that originally
            passed into the constructor.
        
        Args:
            octave (bool): Whether or not to include the octave number.  By
                default, False, i.e. no octave number.

        Returns:
            str: The string representation of the note, dependent on `octave`
        """
        ret = str(self)
        if not octave:
            return ret[:-2]  # Remove two chars for the space and octave number
        return ret
    
    def get_sharp_flat(self) -> int:
        """
        Gets the number of sharps/flats, negative if flats.
        
        Returns:
            int: said number
        """
        if not self.sharp_flat:
            return 0
        return len(self.sharp_flat) * pm_bool(self.sharp_flat[0] == SHARP)
    
    def up_by(self, half_steps: int, scale_length: int) -> Note:
        """
        Get the note half_steps higher than this note.
        
        Args:
            half_steps (int): The number of half steps up from this one that the
                note to get is.
            scale_length (int): The length of the scale (excluding the octave),
                used to determine behaviour regarding whether or not to always
                go up by exactly one letter name.

        Returns:
            Note: The next note in the scale.
        """
        if not 1 <= half_steps <= 3:
            raise Exception(f"BadSizedScaleJumpError: {half_steps}")
        temp_letter = self.letter
        temp_sharp_flat_num = self.get_sharp_flat() + half_steps
        temp_octave = self.octave
        
        match scale_length:
            case 5:   # Pentatonic
                pass
            case 6:   # Whole Tone
                pass
            case 7:   # Most western scales
                temp_letter = get_next_letter(self.letter)
                temp_sharp_flat_num -= 1 if self.letter in ['B', 'E'] else 2
                temp_octave += 1 if self.letter == 'B' else 0
            case 8:   # I can't remember what this one's called, but it's WHx4.
                pass
            case 12:  # Chromatic
                pass
            case _:
                pass
        
        temp_sharp_flat = SHARP*temp_sharp_flat_num + FLAT*-temp_sharp_flat_num
        return Note(f"{temp_letter}{temp_sharp_flat}{temp_octave}")


class Scale:
    pattern: [int]
    starts_on: Note
    display: DesignerObject
    
    def __init__(self, pattern: str, starts_on: str):
        """
        Constructor for Scale.  Creates a scale given a scale pattern and a note
            to start on.
        
        Args:
            pattern: The scale pattern (e.g. WWHWWWH for major)
            starts_on: The note to start on
                (e.g. Ab3 for the A flat just bellow middle-C)
        """
        int_p = [int_from_pattern(c) for c in pattern]
        if ensure_octave(int_p):
            self.pattern = int_p
        else:
            raise Exception(f"InvalidScaleSizeError: {pattern}")
        
        self.starts_on = Note(starts_on)
        self.display = text('red', "", SCALE_TEXT_SIZE)
    
    def __str__(self) -> str:
        """
        Convert the scale to text as simply a list of notes without octaves.

        Returns:
            str: The stringified scale
        """
        this_note = self.starts_on
        disp_text = self.starts_on.string_form()
        for up_by in self.pattern:
            disp_text += " "
            this_note = this_note.up_by(up_by, len(self.pattern))
            disp_text += this_note.string_form()
        return disp_text
    
    def make_text(self, x: int, y: int):
        """
        Create the text for the scale
        
        Args:
            x (int): The x-coordinate of the boulder, and by extension the scale
            y (int): The y-coordinate of the boulder, and by extension the scale
        """
        self.display.x = x
        self.display.y = y
        self.display.text = str(self)

    def move_down(self, speed: int):
        """
        Moves the text down by speed each frame.
        
        Args:
            speed (int): The speed to move the text down by
                It should always be BOULDER_SPEED
        """
        self.display.y += speed
    
    def remove(self):
        destroy(self.display)
        
    
@dataclass
class ScaleInfo:
    name: str  # The name of the type of scale
    pattern: str  # The pattern of whole and half (and augmented) steps
    possible_starts: [str]  # The notes that this type of scale can start on
