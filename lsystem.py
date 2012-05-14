#! /usr/bin/env python
# coding: utf-8

__all__ = ['expand']

def expand(grammar, axiom, times=0):
    """
    Get the l_string of the expanded axiom string N times for the given
    grammar rules
    """
    for n in xrange(times):
        axiom = ''.join( grammar[c] if c in grammar else c for c in axiom )

    return axiom

if __name__ == "__main__":

    # Input: L-System grammar, axiom and apply times
    # Ouput: Generated L-String (stdout)

    # Command line parameters:
    # Axiom (one string parameter)
    # Rules (zero or more string parameters in the form: .:.*)
    # Times (optional integer > 0 parameter)

    pass
