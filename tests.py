#! /usr/bin/env python
# coding: utf-8

from lsystem import expand

import unittest

class TestLSystemExpand(unittest.TestCase):

    def test_empty_grammar_should_not_apply_any_transformation(self):

        grammar = {}
        axiom = 'f+-[]'

        self.assertEquals(axiom, ''.join(expand(grammar, axiom)))

    def test_expand_one_time_should_replace_matches_by_values_once(self):

        grammar = { 'f': '++', '+': ']]', '[': '+]'}
        axiom = 'f+-[]'
        expected = '++]]-+]]'

        self.assertEquals(expected, ''.join(expand(grammar, axiom, 1)))

    def test_expand_several_times_should_replace_matches_by_values_N_times(self):

        grammar = { 'f': '++', '+': ']f', '[': '+]'}
        axiom = 'f+-[]'
        times = 3

        #0: f         +        - [    ]
        #1: +    +    ]  f     - +    ] ]
        #2: ] f  ] f  ]  +  +  - ] f  ] ]
        #3: ] ++ ] ++ ]  ]f ]f - ] ++ ] ]

        expected = ']++]++]]f]f-]++]]'

        self.assertEquals(expected, ''.join(expand(grammar, axiom, times)))

    def test_zero_times_should_always_return_axiom(self):

        grammar = { 'f': '++', '+': ']f', '[': '+]'}
        axiom = 'f+-[]'
        times = 0

        self.assertEquals(axiom, ''.join(expand(grammar, axiom, times)))


if __name__ == "__main__":
    unittest.main()

