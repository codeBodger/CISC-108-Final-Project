# Game Font

This is the font used in the game to display both the scales and the score. 
This font should not be used as a normal font, as most of it is not defined
properly for this.  

### Codepoints
#### Ascii Block
###### Semantic Accidental Symbols
- Flat: b
- Natural: c
- Sharp: #
- Double Sharp: x

###### Numbers
- 0:9: 0:9
- Decimal Point: .
- Minus sign: -

###### Notes
- Two ledger lines below : two above: A:Q / U+0041:U+0051
- Single Whole note: o 
###### Clefs:
- Bass: f
- Treble: g
- C-Clef: h:l

#### Accidentals and Key Signatures Block
###### Ranges
- Flats start at U+00A0
- Naturals start at U+00C0
- Sharps start at U+00E0
- Double Sharps start at U+0100

###### Specs within each Range
- START + 0x00: Blank staff spacer for double accidentals and key signatures
- START + 0x01:0x11: Accidentals ligning up with Notes from A:Q
- START + 0x12: Large accidental symbol
- START + 0x13: Small accidental symbol
- START + 0x14:0x1f: Unused, blank
