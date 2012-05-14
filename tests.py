#! /usr/bin/env python
# coding: utf-8

from lsystem import expand
import unittest

class TestLSystemExpand(unittest.TestCase):

    def test_empty_grammar_should_not_apply_any_transformation(self):

        grammar = {}
        axiom = 'AXIOM'

        self.assertEquals(axiom, expand(grammar, axiom))

    def test_expand_one_time_should_replace_matches_by_values_once(self):

        grammar = { 'A': 'XX', 'X': 'MM', 'O': 'XM'}
        axiom = 'AXIOM'
        expected = 'XXMMIXMM'

        self.assertEquals(expected, expand(grammar, axiom, 1))

    def test_expand_several_times_should_replace_matches_by_values_N_times(self):

        grammar = { 'A': 'XX', 'X': 'MA', 'O': 'XM'}
        axiom = 'AXIOM'
        times = 3

        #0: A         X        I O    M
        #1: X    X    M  A     I X    M M
        #2: M A  M A  M  X  X  I M A  M M
        #3: M XX M XX M  MA MA I M XX M M

        expected = 'MXXMXXMMAMAIMXXMM'

        self.assertEquals(expected, expand(grammar, axiom, times))

    def test_zero_times_should_always_return_axiom(self):

        grammar = { 'A': 'XX', 'X': 'MA', 'O': 'XM'}
        axiom = 'AXIOM'
        times = 0

        self.assertEquals(axiom, expand(grammar, axiom, times))

if __name__ == "__main__":
    unittest.main()
