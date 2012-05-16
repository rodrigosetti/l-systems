#! /usr/bin/env python
# coding: utf-8

from lsystem import *
import unittest

class TestExpand(unittest.TestCase):

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

    def test_non_terminal_chars_should_be_left_out(self):

        grammar = { 'f': 'AA', 'A': 'Bf', '[': 'AB'}
        axiom = 'fA-[B'
        times = 3

        #0: f         A        - [    B
        #1: A    A    B  f     - A    B B
        #2: B f  B f  B  A  A  - B f  B B
        #3: B AA B AA B  Bf Bf - B AA B B

        expected = 'ff-'

        self.assertEquals(expected, ''.join(expand(grammar, axiom, times)))

class TestCommands(unittest.TestCase):

    def test_commands_should_return_a_tuple_for_each_command(self):

        l_string = '<-f[+]>'
        length = 10
        delta_theta = 25
        expected = [(TURN_Z, -25), (TURN_Y, -25), (MOVE, 10), ('[', None), (TURN_Y, 25), (']', None), (TURN_Z, 25)]

        self.assertEquals( expected, list(commands(l_string, length, delta_theta)) )

    def test_commands_should_accumulate_moves(self):

        l_string = 'ffffffffff'
        length = 10
        delta_theta = 25
        expected = [(MOVE, 100)]

        self.assertEquals( expected, list(commands(l_string, length, delta_theta)) )

    def test_commands_should_accumulate_turns(self):

        l_string = '+-++-+<<<><<>>'
        length = 10
        delta_theta = 25
        expected = [(TURN_Y, 50), (TURN_Z, -50)]

        self.assertEquals( expected, list(commands(l_string, length, delta_theta)) )

    def test_commands_should_drop_zero_turns(self):

        l_string = '+-++-+--<<<><><>>>'
        length = 10
        delta_theta = 25
        expected = []

        self.assertEquals( expected, list(commands(l_string, length, delta_theta)) )

    def test_commands_should_drop_zero_and_collapse_before_and_after(self):

        l_string = 'f<>f'
        length = 10
        delta_theta = 25
        expected = [(MOVE, 20)]

        self.assertEquals( expected, list(commands(l_string, length, delta_theta)) )



if __name__ == "__main__":
    unittest.main()

