#! /usr/bin/env python
# coding: utf-8

from lsystem import expand
import unittest

class TestLSystemExpand(unittest.TestCase):

    def test_empty_grammar_should_not_apply_any_transformation(self):

        grammar = {}
        axiom = 'AXIOM'
        expected = 'AXIOM'

        self.assertEquals(expected, expand(grammar, axiom))

    def test_expand_one_time_should_replace_matches_by_values_once(self):

        grammar = { 'A': 'XX', 'X': 'MM', 'O': 'XM'}
        axiom = 'AXIOM'
        expected = 'XXMMIXMM'

        self.assertEquals(expected, expand(grammar, axiom, 1))

if __name__ == "__main__":
    unittest.main()

