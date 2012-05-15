#! /usr/bin/env python
# coding: utf-8

from __future__ import division
import transformation
import numpy

# states/commands
MOVE = 'f'
TURN_Y = 'y'
TURN_Z = 'z'

def commands(l_string, length, delta_theta):
    "Group commands from l_string"

    last_state = state = None
    how_much = amount = 0

    for c in l_string:

        if c in '[]':
            if how_much != 0:
                yield (last_state, how_much)
            how_much = 0
            yield (c, None)
            continue
        elif c == 'f':
            state = MOVE
            amount = length
        elif c in '+-':
            state = TURN_Y
            amount = delta_theta if c == '+' else -delta_theta
        elif c in '><':
            state = TURN_Z
            amount = delta_theta if c == '>' else -delta_theta
        else:
            continue

        if last_state != state:
            if how_much != 0:
                yield (last_state, how_much)
            how_much = amount
        else:
            how_much += amount

        last_state = state

    # last state
    if how_much != 0:
        yield (last_state, how_much)

def paths(l_string, length, delta_theta, origin=(0,0,0,1)):
    """
    Yield a sequence of paths of 3D points for a plot of a given l_string
    """
    matrix = transformation.identity_matrix()
    state_stack = []
    path = [origin]

    for c, amount in commands(l_string, length, delta_theta):
        if c == '[':
            state_stack.append( (matrix, path) )
            path = [ numpy.dot(matrix, origin) ]
        elif c == ']':
            yield path
            matrix, path = state_stack.pop()
        elif c == MOVE:
            matrix = numpy.dot(matrix, transformation.translation_matrix( (0, -amount, 0) ))
            path.append( numpy.dot(matrix, origin) )
        elif c == TURN_Y:
            matrix = numpy.dot(matrix, transformation.rotation_matrix(amount, (0,0,1)))
        elif c == TURN_Z:
            matrix = numpy.dot(matrix, transformation.rotation_matrix(amount, (0,1,0)))

    # yields last path
    yield path


if __name__ == "__main__":

    import sys
    from math import radians
    from PIL import Image, ImageDraw

    from optparse import OptionParser

    # Read grammar rules and application times from command line parameters
    parser = OptionParser()
    parser.add_option("-l", "--length", dest="length", action="store", default=1, type="float",
                       help="Length of the segments", metavar="LENGTH")
    parser.add_option("-a", "--angle", dest="angle", action="store", default=60, type="float",
                       help="Angle of turns (degrees)", metavar="ANGLE")
    parser.add_option("-f", "--filename", dest="filename", action="store", default='out.png',
                       help="Filename to save the image", metavar="FILE")

    (options, args) = parser.parse_args()

    # if there is one argument and it's not "-"
    if args and args[0] != '-':
        # read contents from file
        l_string = open(args[0]).read()
    else:
        # read contents from stdin
        l_string = sys.stdin.read()

    # get coordinates
    paths = tuple(paths( l_string, float(options.length), radians(float(options.angle))))

    # define size
    min_x = min( min(point[0] for point in path) for path in paths)
    max_x = max( max(point[0] for point in path) for path in paths)
    min_y = min( min(point[1] for point in path) for path in paths)
    max_y = max( max(point[1] for point in path) for path in paths)

    # create new image
    image = Image.new( 'RGB', (int(max_x-min_x), int(max_y-min_y)))
    draw = ImageDraw.Draw(image)

    for path in paths:
        draw.line( [(p[0]-min_x, p[1]-min_y) for p in path], (255,255,255) )

    image.save( options.filename, "PNG" )

