#! /usr/bin/env python
# coding: utf-8

__all__ = ['expand']

def expand(grammar, axiom, times=1):
    """
    Get the l_string of the expanded axiom string N times for the given
    grammar rules
    """
    for n in xrange(times):
        axiom = sum( (list(grammar[c]) if c in grammar else [c] for c in axiom), [] )

    return ''.join(axiom)

if __name__ == "__main__":

    # Input: L-System grammar, axiom and apply times
    # Ouput: Generated L-String (stdout)

    import sys
    from optparse import OptionParser

    # Read grammar rules and application times from command line parameters
    parser = OptionParser()
    parser.add_option("-r", "--rule", dest="rules", action="append",
                       help="Adds a grammar rule in the for .:.*", metavar="RULE")
    parser.add_option("-t", "--times", dest="times", action="store", default=1, type="int",
                       help="The number of times the grammar will be applied", metavar="TIMES")

    (options, args) = parser.parse_args()

    # if there is one argument and it's not "-"
    if args and args[0] != '-':
        # read contents from file
        axiom = open(args[0]).read()
    else:
        # read contents from stdin
        axiom = sys.stdin.read()

    # create grammar
    grammar = dict( rule.split(':') for rule in options.rules)

    # print produced l-string:
    print expand( grammar, axiom, int(options.times))

