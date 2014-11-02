"""
Convert the GPS data from a set of images to a CSV file.

Note that CSV import to Google Maps has a 500 row limit (or 2000 for Maps Pro)
"""


import argparse
import csv
import sys

from pexif import JpegFile


def get_all_image_points(filename_format, first=0, last=None):
    """
    Gets all GPS points for a given set of images.

    Each point is a dict of {image_id, lat, lon, image_filename}

    @param filename_format Filename format for images
    @param first Index of image at start of range
    @param last Index of iimage at end of range
    @returns List of GPS points maintaining image order
    """

    points = list()

    # If no end index was defined just continue the loop until we get an error
    if last is None:
        last = sys.maxint

    print 'Getting points from images with format: %s' % filename_format
    print '\t(first index = %d, last index = %d)' % (first, last)

    for frame_no in xrange(first, last):
        filename = filename_format % frame_no

        # Try to open the image, if it fails assume this is the end of a range
        try:
            exif = JpegFile.fromFile(filename)
        except IOError:
            break

        gps_pos = exif.get_geo()

        point = dict()
        point['index'] = frame_no
        point['image_filename'] = filename
        point['lat'] = gps_pos[0]
        point['lon'] = gps_pos[1]

        points.append(point)

    return points


def reduce_points(input_points, max_points=None):
    """
    Takes a list of points and reduces the number of points to no larger than max_points.

    @param input_points List of input points
    @param max_points Number of points desired in output
    @returns List of points
    """

    # Default to 500 points
    if max_points is None:
        max_points = 500

    print 'Reducing point count (max %d)' % max_points

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

    print 'Saving CSV file: %s' % filename

    # Open the CSV file
    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        # Write a header
        writer.writerow(['frame_index', 'lat', 'lon', 'image_filename'])

        # Write each point
        for point in points:
            writer.writerow([point['index'], point['lat'], point['lon'], point['image_filename']])


def run(params):
    """
    Runs the script.

    @param params Arguments
    """

    all_points = get_all_image_points(params.file_pattern, params.start_image, params.end_image)

    if params.verbose:
        print 'All points from file:'
        for point in all_points:
            print point

    reduced_points = reduce_points(all_points, params.max_points)

    if params.verbose:
        print 'All reduced points:'
        for point in reduced_points:
            print point

    save_csv(reduced_points, params.csv_file)


def get_parameters():
    """
    Gets parameters.

    @returns Arguments
    """

    parser = argparse.ArgumentParser(description='Image GPS EXIF to CSV converter.')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Prints more output to console'
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

    parser.add_argument(
        '--max-points',
        action='store',
        type=int,
        help='Maximum number of data points in CSV outout',
        metavar='N'
    )

    props = parser.parse_args()
    return props


if __name__ == '__main__':
    params = get_parameters();

    if params.file_pattern is None:
        raise ValueError('No filename pattern given')

    run(params)
