#! /usr/bin/env python
# coding: utf-8

from __future__ import division

from PIL import Image, ImageDraw
from math import radians
import json, numpy, math

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

# Copyright requirements For the use of functions: translation_matrix,
# rotation_matrix and unit_vector:
#
# Copyright (c) 2006-2012, Christoph Gohlke
# Copyright (c) 2006-2012, The Regents of the University of California
# Produced at the Laboratory for Fluorescence Dynamics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

def translation_matrix(direction):
    "Return matrix to translate by direction vector."
    M = numpy.identity(4)
    M[:3, 3] = direction[:3]
    return M

def unit_vector(data, axis=None, out=None):
    "Return ndarray normalized by length, i.e. eucledian norm, along axis."
    if out is None:
        data = numpy.array(data, dtype=numpy.float64, copy=True)
        if data.ndim == 1:
            data /= math.sqrt(numpy.dot(data, data))
            return data
    else:
        if out is not data:
            out[:] = numpy.array(data, copy=False)
        data = out
    length = numpy.atleast_1d(numpy.sum(data*data, axis))
    numpy.sqrt(length, length)
    if axis is not None:
        length = numpy.expand_dims(length, axis)
    data /= length
    if out is None:
        return data

def rotation_matrix(angle, direction, point=None):
    "Return matrix to rotate about axis defined by point and direction."
    sina = math.sin(angle)
    cosa = math.cos(angle)
    direction = unit_vector(direction[:3])
    # rotation matrix around unit vector
    R = numpy.diag([cosa, cosa, cosa])
    R += numpy.outer(direction, direction) * (1.0 - cosa)
    direction *= sina
    R += numpy.array([[ 0.0,         -direction[2],  direction[1]],
                      [ direction[2], 0.0,          -direction[0]],
                      [-direction[1], direction[0],  0.0]])
    M = numpy.identity(4)
    M[:3, :3] = R
    if point is not None:
        # rotation not around origin
        point = numpy.array(point[:3], dtype=numpy.float64, copy=False)
        M[:3, 3] = point - numpy.dot(R, point)
    return M

#########

def get_paths(l_string, length, delta_theta, origin=(0,0,0,1)):
    """
    Yield a sequence of paths of 3D points for a plot of a given l_string
    """
    matrix = numpy.identity(4)
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
            matrix = numpy.dot(matrix, translation_matrix( (0, -amount, 0) ))
            path.append( numpy.dot(matrix, origin) )
        elif c == TURN_Y:
            matrix = numpy.dot(matrix, rotation_matrix(amount, (0,0,1)))
        elif c == TURN_Z:
            matrix = numpy.dot(matrix, rotation_matrix(amount, (0,1,0)))

    # yields last path
    yield path

def process_file(file_obj, default_out_filename='out.png'):
    """
    Reads from the file object, process the configuration, plots the L-system
    and saves to the default_out_filename if there is not a filename config
    """
    config = json.load( file_obj )

    # expand string
    l_string = expand( config['rules'], config['axiom'], config['applies'])

    # get coordinates
    paths = tuple(get_paths( l_string, float(config['length']), radians(float(config['angle']))))

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

    image.save( config['filename'] if 'filename' in config else default_out_filename, "PNG" )

if __name__ == "__main__":

    import sys

    # if there is one argument and it's not "-"
    if len(sys.argv) > 1 and sys.argv[1] != '-':
        # process each filename in input
        for filename in sys.argv[1:]:
            with open(filename) as f:
                process_file( f, filename.split('.')[0] + '.png')
    else:
        # read contents from stdin
        process_file( sys.stdin )

