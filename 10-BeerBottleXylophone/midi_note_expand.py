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
    logger.info('Output file: %s' % output_file)

    # Give error if no minimum time was provided
    if params.delay is None:
        logger.error('No minimum time delay was provided')
        exit(1)

    pass


if __name__ == '__main__':
    run()
