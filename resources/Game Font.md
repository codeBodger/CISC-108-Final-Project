# Game Font

This is the font used in the game to display both the scales and the score. 
This font should not be used as a normal font, as most of it is not defined
properly for this.  

### Codepoints
#### Ascii Block
###### Semantic Accidental Symbols
- Flat: b
- Natural: h
- Sharp: #
- Double Sharp: x

###### Numbers
- 0:9: 0:9
- Decimal Point: .
- Minus sign: -

###### Notes
- Two ledger lines below : two above: U+E001:U+E011
- Single Whole note: o 
###### Clefs:
- Bass: U+E0A9
- Treble: U+E0AE
- C-Clef:
  - Baritone: U+E0AB
  - Tenor: U+E0AD
  - Alto: U+E0AF
  - Mezzo-soprano: U+E0AA
  - Soprano: U+E0AC

#### Accidentals and Key Signatures Block
###### Ranges
- Flats start at U+E020
- Naturals start at U+E040
- Sharps start at U+E060
- Double Sharps start at U+E080

###### Specs within each Range
- START + 0x00: Blank staff spacer for double accidentals and key signatures
- START + 0x01:0x11: Accidentals ligning up with Notes from A:Q
- START + 0x12: Large accidental symbol
- START + 0x13: Small accidental symbol
- START + 0x14:0x1f: Unused, blank
