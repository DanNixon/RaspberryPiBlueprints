"""
A tool for getting the MIDI notes used in a file.
"""

import sys
import midi


def get_midi_note_name(midi_note):
    """
    Gets a friedly name for a MIDI note.

    @param midi_note MIDI note ID
    @return Note as string
    """

    note_index = midi_note % midi.NOTE_PER_OCTAVE
    octave = (midi_note / midi.OCTAVE_MAX_VALUE) - 1
    note_name = midi.NOTE_NAMES[note_index]
    return '%s_%d' % (note_name, octave)


if len(sys.argv) < 2:
    print 'Usage %s <MIDI file>' % sys.argv[0]
    exit(1)

# Open the input MIDI file
pattern = midi.read_midifile(sys.argv[1])

# Keep track of the notes used
notes_used = set()

# Read the file
for track in pattern:
    for event in track:
        if isinstance(event, midi.NoteOnEvent):
            pitch = event.data[0]
            notes_used.add(pitch)

# Output the notes used in MIDI file
print 'Number of unique notes: %d' % len(notes_used)
print 'Notes: %s' % str(notes_used)
print 'Notes: %s' % str([get_midi_note_name(note) for note in notes_used])
