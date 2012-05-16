#! /usr/bin/env python
# coding: utf-8

from __future__ import division
import transformation
import numpy

TERMINALS = 'fg+-><[]'

def expand(grammar, axiom, times=1):
    """
    Get the l_string of the expanded axiom string N times for the given
    grammar rules
    """
    for n in xrange(times):
        axiom = sum( (list(grammar[c]) if c in grammar else [c] for c in axiom), [] )

    return (c for c in axiom if c in TERMINALS)

# states/commands
MOVE = 'f'
TURN_Y = 'y'
TURN_Z = 'z'

def commands(l_string, length, delta_theta):
    "Group commands from l_string"

    commands = []

    for c in l_string:

        if c in '[]':
            command, amount = c, None
        elif c in 'fg':
            command, amount = MOVE, length
        elif c in '+-':
            command = TURN_Y
            amount = delta_theta if c == '+' else -delta_theta
        elif c in '><':
            command = TURN_Z
            amount = delta_theta if c == '>' else -delta_theta
        else:
            # not command character
            continue

        if commands:
            if command not in '[]' and commands[-1][0] == command:
                # agregate
                commands[-1] = (commands[-1][0], commands[-1][1] + amount)

                # if aggregation yielded a zero command, then drop it
                if commands[-1][1] == 0:
                    commands.pop()

                continue

        commands.append( (command, amount) )

    return commands

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

    import sys, json
    from math import radians
    from PIL import Image, ImageDraw

    # if there is one argument and it's not "-"
    if len(sys.argv) > 1 and sys.argv[1] != '-':
        # read contents from file
        config = json.load(open( sys.argv[1] ))
        filename = sys.argv[1].split('.')[0] + '.png'
    else:
        # read contents from stdin
        filename = 'out.png'
        config = json.load(sys.stdin)

    # expand string
    l_string = expand( config['rules'], config['axiom'], config['applies'])

    # get coordinates
    paths = tuple(paths( l_string, float(config['length']), radians(float(config['angle']))))

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

    image.save( config['filename'] if 'filename' in config else filename, "PNG" )

