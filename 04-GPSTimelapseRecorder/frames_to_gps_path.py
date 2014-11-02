"""
Convert the GPS data from a set of images to a CSV file.

Note that CSV import to Google Maps has a 500 row limit (or 2000 for Maps Pro)
"""


import argparse

import pexif


def get_all_image_points(filename_format, first=0, last=None):
    """
    Gets all GPS points for a given ste of images.

    Each point is a dict of {image_id, lat, lon, image_filename}

    @param filename_format Filename format for images
    @param first Index of image at start of range
    @param last Index of iimage at end of range
    @returns List of GPS points maintaining image order
    """

    points = list()

    # TODO

    return points


def reduce_points(input_points, max_points=500):
    """
    Takes a list of points and reduces the number of points to no larger than max_points.

    @param input_points List of input points
    @param max_points Number of points desired in output
    @returns List of points
    """

    # If input already has less points then there is nothing to do
    if len(input_points) <= max_points:
        return input_points

    out_points = list()

    # TODO

    return out_points


def save_csv(points, filename):
    """
    Saves a set of GPS points to a CSV file.

    @param points GPS points
    @param filename Filename for CSV file
    """

    pass


def run(params):
    """
    Runs the script.

    @param params Arguments
    """

    print params


def get_parameters():
    """
    Gets parameters.

    @returns Arguments
    """

    parser = argparse.ArgumentParser(description='Image GPS EXIF to CSV converter.')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Increases console verbosity'
    )

    parser.add_argument(
        '-f', '--file-pattern',
        action='store',
        help='Specifies folder and filename pattern for source images'
    )

    parser.add_argument(
        '-o', '--csv-file',
        action='store',
        default='gps_points.csv',
        help='Specifies filename for output CSV file'
    )

    parser.add_argument(
        '--start-image',
        action='store',
        type=int,
        default=0,
        help='Index of first frame',
        metavar='N'
    )

    parser.add_argument(
        '--end-image',
        action='store',
        type=int,
        help='Index of last frame',
        metavar='N'
    )

    props = parser.parse_args()
    return props


if __name__ == '__main__':
    params = get_parameters();

    if params.file_pattern is None:
        raise ValueError('No filename pattern given')

    run(params)
