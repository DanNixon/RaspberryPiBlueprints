"""
A tool for expanding the time between a MIDI note on and note off event.

Note on events with a velocity of zero are treated as note off events.
The minimum time given is only valid for the tempo provided, at worst the highest playback tempo should be provided
"""

import argparse
import logging
import os
import midi


logger = logging.getLogger(__file__)


def get_parameters():
    """
    Gets parameters.

    @returns Arguments
    """

    parser = argparse.ArgumentParser(description='Expands the time between a note on and note off MIDI event')

    parser.add_argument(
        '-l', '--log-level',
        action='store',
        default='INFO',
        help='Selects logging level for console log'
    )

    parser.add_argument(
        '-f', '--input-file',
        action='store',
        help='Specifies the MIDI file to modify'
    )

    parser.add_argument(
        '-o', '--output-file',
        action='store',
        help='Specifies filename for the modified file'
    )

    parser.add_argument(
        '-t', '--tempo',
        action='store',
        type=int,
        default=60,
        help='Tempo at which the file will be played back (In BPM)',
        metavar='T'
    )

    parser.add_argument(
        '-d', '--delay',
        action='store',
        type=int,
        help='Minimum time required between note on and note off (in ms)',
        metavar='T'
    )

    props = parser.parse_args()
    return props


def run():
    """
    Runs the script.
    """

    params = get_parameters();

    log_level = getattr(logging, params.log_level.upper(), None)
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    # Give error if no input file was provided
    if params.input_file is None:
        logger.error('No input file provided')
        exit(1)

    # Get the output file name from parameters or use default value
    if params.output_file is None:
        input_file_data = os.path.splitext(params.input_file)
        output_file = '%s_modified%s' % (input_file_data[0], input_file_data[1])
    else:
        output_file = params.output_file

    # Give error if no minimum time was provided
    if params.delay is None:
        logger.error('No minimum time delay was provided')
        exit(1)

    # Open the input MIDI file
    pattern = midi.read_midifile(params.input_file)
    pattern.make_ticks_abs()

    # Calculate number of ticks in a millisecond and minumum required ticks between noes
    ticks_per_ms = (pattern.resolution * 1000.0) / (60 * 1000000.0 / params.tempo)
    logger.info('Ticks per ms for resolution %f and BPM %d = %f' % (pattern.resolution, params.tempo, ticks_per_ms))
    delta_tick_min = int(params.delay * ticks_per_ms + 1.0)
    logger.info('Minumum ticks between note on and off = %f' % delta_tick_min)

    # Keep track of the active notes
    notes_on = dict()

    # Expand note durations
    for track in pattern:
        # Keep track of how many note events have been changed
        changed_notes = 0

        for event in track:
            # Marker indicating if a note on event has a zero velocity
            zero_note_on = False

            # Process a note on message
            if isinstance(event, midi.NoteOnEvent):
                pitch = event.data[0]
                if event.data[1] > 0 and pitch not in notes_on:
                    notes_on[pitch] = event.tick
                else:
                    zero_note_on = True

            # Process a note off message
            if isinstance(event, midi.NoteOffEvent) or zero_note_on:
                pitch = event.data[0]

                # Check if the note is on
                if pitch in notes_on:
                    # See how long it has been on for
                    note_on_tick = notes_on.pop(pitch)
                    delta_tick = event.tick - note_on_tick
                    logger.debug('Tick delta for note %d = %d' % (pitch, delta_tick))

                    # If it was too short then change the note off time
                    if delta_tick < delta_tick_min:
                        event.tick = note_on_tick + delta_tick_min
                        changed_notes += 1

        # MIDI expects the events to be in order
        track.sort()

        logger.info('Changed %d notes over track' % (changed_notes))

    # Save output MIDI file
    pattern.make_ticks_rel()
    midi.write_midifile(output_file, pattern)
    logger.info('Saved output MIDI file: %s' % output_file)


if __name__ == '__main__':
    run()
