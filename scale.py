# Imports for type checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Normal imports
from designer import *
from useful_funcs import int_from_pattern, ensure_octave, get_next_letter, \
    pm_bool, cmp
from dataclasses import dataclass


# I might change these to better symbols at some point.
SHARP = '#'
FLAT  = 'b'

SCALE_TEXT_SIZE = 30
BACKGROUND_WIDTH  = 176
BACKGROUND_HEIGHT = 60

ORDER_OF_SHARPS = 'FCGDAEB'
LETTERS_PER_OCTAVE = len(ORDER_OF_SHARPS)

NOTES_START = 0xE000
FLATS_START = 0xE020
NATURALS_START = 0xE040
SHARPS_START = 0xE060
ACCIDENTALS_START = {
    SHARP: SHARPS_START,
    FLAT: FLATS_START
}


@dataclass
class Clef:
    name: str
    symbol: str
    lowest_note: Note  # Note number 1, not 0
    sharps_pattern: [bool]  # True: up   a 5th, False: down a 4th
    flats_pattern: [bool]  # True: down a 5th, False: up   a 4th


class KeySignature:
    sharps_flats: int
    
    def __init__(self, sharps_flats: int = 0):
        """
        Constructor for KeySignature.  Just assigns the input to the field.

        Args:
            sharps_flats (int): The number of sharps or flats in the key
                signature.  Positive for sharps, negative for flats.
        """
        self.sharps_flats = sharps_flats
    
    def __contains__(self, note: Note) -> bool:
        """
        Tests if the letter of note is in the key signature.

        Args:
            note (Note): The note to test about

        Returns:
            bool: Whether or not the letter of note is in the key signature.
        """
        if self.sharps_flats < 0:
            return note.letter in ORDER_OF_SHARPS[self.sharps_flats:]
        return note.letter in ORDER_OF_SHARPS[:self.sharps_flats]
    
    def __rxor__(self, note: Note) -> bool:
        """
        Using this to see if a Note and this key signature have the same type.
            I.e. we should have already determined if the Note was in the key
            signature, and we're now checking if the accidental on the note is
            different from what they key signature would make it.
        
        Args:
            note (Note): The note to compare to this key signature

        Returns:
            bool: Whether or not the accidental and key signature are different
        """
        if note not in self:
            raise KeyError(
                "NoteNotEffectedByKeySignatureError: "
                f"Note: {str(note)}, KeySignature: {self.sharps_flats}"
            )
        #             Type of accidental        !=   type of key signature
        return -cmp(f"{note.sharp_flat}A", "A") != cmp(self.sharps_flats, 0)


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
    
    def font_offset_number(self, clef: Clef) -> int:
        """
        Gets the amount to shift from the base character in the font.  When
            added to NOTES_START, FLATS_START, NATURALS_START, etc, gives the
            correct symbol.  I.e. how high on the staff the note needs to be.
        
        Args:
            clef (Clef): The clef that the note will be displayed in, so we know
                how high on the staff it needs to be.

        Returns:
            int: How high on the staff the note needs to be, given the clef.
        """
        octave_diff = self.octave - clef.lowest_note.octave
        # Deal with the fact that octaves change at C, not at A
        octave_diff += (self.letter < 'C') - (clef.lowest_note.letter < 'C')
        # +1, because the lowest_note is number 1, not 0
        note_diff = ord(self.letter) - ord(clef.lowest_note.letter) +1
        return octave_diff * LETTERS_PER_OCTAVE + note_diff
    
    def accidentals_symbols(self, clef: Clef, with_natural: bool = True) -> str:
        """
        Gets the symbols to display the accidentals of this note, given the clef
            and whether or not to also display naturals.
            Note: since the font has no width for accidentals, multiple flats
            will look like one flat and many sharps will look either like one
            double sharp, or a double sharp overlaid on a single sharp.
        
        Args:
            clef (Clef): The clef with respect to which to find the characters
                for the accidentals.
            with_natural (bool): Whether or not to display naturals, or leave
                them blank.  By default, True, displaying them.

        Returns:
            str: The accidentals to display.
        """
        if not self.sharp_flat:
            if not with_natural:
                return ""
            return chr(NATURALS_START + self.font_offset_number(clef))
        accidental = self.sharp_flat[0]
        char_ind = ACCIDENTALS_START[accidental] + self.font_offset_number(clef)
        return self.sharp_flat.replace(accidental, chr(char_ind))
    
    def string_form(self,
                    clef: Clef = None,
                    key_signature: KeySignature = KeySignature(),
                    octave: bool = False
                    ) -> str:
        """
        Makes a string version of the note, very similar to that originally
            passed into the constructor, if no clef is specified.
        If a clef is specified, a version of the Note that can be displayed as
            sheet music with Game Font is returned.
        
        Args:
            clef (Clef): The clef with respect to which to make a string for the
                note.  By default, None, in which case a text version is given,
                instead of one to be displayed with Game Font.
            key_signature (KeySignature): The key signature to use to see if an
                accidental needs to be displayed.
            octave (bool): Whether or not to include the octave number.  By
                default, False, i.e. no octave number.

        Returns:
            str: The string representation of the note, either a plain text form
                or one to be displayed with Game Font.
        """
        if clef is not None:
            accidental = ""
            if self in key_signature:
                if self ^ key_signature:
                    accidental = self.accidentals_symbols(clef)
            else:
                accidental = self.accidentals_symbols(clef, with_natural=False)
            note_on_staff = chr(NOTES_START + self.font_offset_number(clef))
            return accidental + note_on_staff
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
            raise ValueError(f"BadSizedScaleJumpError: {half_steps}")
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


CLEFS = {
    "bass":   Clef("bass",   '\uE0A9', Note("C2"),
                   [False, True, False, True, False, True],
                   [False, True, False, False, True, False]
                   ),
    "treble": Clef("treble", '\uE0AE', Note("A3"),
                   [False, True, False, True, False, True],
                   [False, True, False, False, True, False]
                   )
}


class Scale:
    pattern: [int]
    starts_on: Note
    clef: Clef
    key_signature: KeySignature
    background: DesignerObject
    display: DesignerObject
    
    def __init__(self, pattern: str, starts_on: str, clef: str = "treble"):
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
        self.clef = CLEFS[clef]
        self.background = rectangle('white',
                                    BACKGROUND_WIDTH,BACKGROUND_HEIGHT)
        self.display = text(
            'black', "", SCALE_TEXT_SIZE,
            font_name="Game Font", font_path="Game Font.ttf"
        )
    
    def __str__(self) -> str:
        """
        Convert the scale to sheet music in Game Font

        Returns:
            str: The sheet music scale
        """
        this_note = self.starts_on
        disp_text = self.clef.symbol
        for up_by in self.pattern + [2]:  # The 2 is just so it runs again
            disp_text += this_note.string_form(self.clef)
            this_note = this_note.up_by(up_by, len(self.pattern))
        return disp_text
    
    def __repr__(self) -> str:
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
        
        if "Fb" in disp_text:
            print("hi")
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
        
        self.background.x = x
        self.background.y = y - 10
        self.background.width = 176
        self.background.height = 60

    def move_down(self, speed: float):
        """
        Moves the text down by speed each frame.
        
        Args:
            speed (int): The speed to move the text down by
                It should always be BOULDER_SPEED
        """
        self.display.y += speed
        self.background.y += speed
    
    def remove(self):
        destroy(self.display)
        
    
@dataclass
class ScaleInfo:
    name: str  # The name of the type of scale
    pattern: str  # The pattern of whole and half (and augmented) steps
    possible_starts: [str]  # The notes that this type of scale can start on
