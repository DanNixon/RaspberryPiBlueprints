import argparse
import os
import random
import sys
import subprocess


def play_file(filename, frequency):
    """
    Plays a given MP3 file using ffmpeg and PiFM.

    @param filename Path to MP3 to play
    @param frequency Frequency to broadcast at
    """

    print 'Broadcasting %s at %f MHz' % (filename, frequency)

    command = 'ffmpeg -i "%s" -f s16le -ar 22.05k -ac 2 - | sudo ./pifm - %f 22050 stereo' % (filename, frequency)
    subprocess.call(command, shell=True)


def get_mp3_files(directory):
    """
    Gets a list of all MP3 files in a directory (and it's subdirectories).

    @param directory The base directory to search
    """

    mp3_files = list()

    for root, dirs, files in os.walk(directory):
        # For all filenames in the directory
        for filename in files:
            # Check if it is an MP3
            if filename.endswith(".mp3"):
                # Add it to the list
                mp3_files.append(os.path.join(root, filename))

    return mp3_files


def run(params):
    """
    Search for files and play them according to options selected.

    @param params Program parameters
    """

    # Get a list of MP3s
    filenames = get_mp3_files(params.directory)

    file_number = -1
    while True:
        # Get the index for the next track based on the playback
        if params.random:
            file_number = random.randint(0, len(filenames))
        else:
            file_number += 1
            # Stop when we run out of files
            if file_number >= len(filenames):
                return

        # Broadcast the MP3
        play_file(filenames[file_number], params.frequency)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Broadcast a set of MP3s over FM')

    parser.add_argument(
            '--random',
            action='store_true',
            help='Play in random order')

    parser.add_argument(
            '-f', '--frequency',
            default=101.1,
            type=float,
            help='Frequency on which to broadcast')

    parser.add_argument(
            '-d', '--directory',
            default='.',
            type=str,
            help='Directory to search for MP3 file')

    params = parser.parse_args()
    run(params)
