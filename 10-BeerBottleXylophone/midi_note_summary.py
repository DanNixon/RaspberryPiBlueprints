"""
A tool for getting the MIDI notes used in a file.
"""

import sys
import midi


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
print 'Notes: %s' % str(list(notes_used))
