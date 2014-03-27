Lindenmayer Systems
===================

What is it?
-----------

An L-system or Lindenmayer system is a parallel rewriting system,
namely a variant of a formal grammar, most famously used to model the
growth processes of plant development, but also able to model the
morphology of a variety of organisms. A L-system consists of an
alphabet of symbols that can be used to make strings, a collection of
production rules which expand each symbol into some larger string of
symbols, an initial "axiom" string from which to begin construction,
and a mechanism for translating the generated strings into geometric
structures. L-systems can also be used to generate self-similar fractals
such as iterated function systems. L-systems were introduced and
developed in 1968 by the Hungarian theoretical biologist and botanist
from the University of Utrecht, Aristid Lindenmayer. (from Wikipedia:
http://en.wikipedia.org/wiki/L-system)

Implementation
--------------

This is a simple implementation of the L-System. The goal is to produce
both 2D and 3D images with several configuration settings (_i. e._
color, thickness, etc.) and, possibly, with different output options
(_i. e._ Standard image types, 3D Models, Povray scene, etc.).

The program might follow UNIX philosophy: Do one thing and do it well.
In this context, this project will not attempt to create a fancy user
interface or facilities to edit L-System rules. Instead, it should focus
on robustness, being fast and several output options. Other tools could
be built and used to aid users edit L-Systems rules. This one, just take
them as input.

The program `lsystem.py` accepts one or more filenames as command line
arguments or it reads from `stdin`. The contents of the file is a JSON
with configurations for the L-System parameters as an object, _e.g._:

```json
{
    "axiom": "X",
    "applies": 6,
    "angle": 25,
    "length": 10,
    "rules" : {
        "X": "f-[[X]+X]+f[+fX]-X",
        "f": "ff"
    }
}
```

These are the supported configuration keys:

  * "axiom": The starting string of the L-System.
  * "applies": The number of times the rules are applied to the string.
  * "angle": The angle to apply for the turning commands. In degrees.
  * "length": The length of each `f` command. In pixels.
  * "rules": A dictionary of character and substitution strings.

These are the supported commands:

  * `f` or `g`: move forward.
  * `+`: turn `angle` right.
  * `-`: turn `angle` left.
  * `[`: Start branch.
  * `]`: End branch (and restore orientation when branch was started)

TODO
----

  * Support context sensitive grammars
  * Support stochastic grammars
  * Initial angle heading
  * Image margins, colors and thickness configuration

Examples
--------

The formulas for these examples are in the `examples` folder.

Three examples from Lindenmayer _et. al._ book [The Algorithmic Beauty of
Plants](http://en.wikipedia.org/wiki/The_Algorithmic_Beauty_of_Plants):

![Plant 1](images/plant-1.png?raw=true)
![Plant 2](images/plant-2.png?raw=true)
![Plant 3](images/plant-3.png?raw=true)

The [Koch Snowflake](http://en.wikipedia.org/wiki/Koch_snowflake):

![Koch Snowflake](images/koch-snowflake.png?raw=true)

The [Sierpinski triangle](http://en.wikipedia.org/wiki/Sierpinski_triangle):

![Sierpinski Triangle](images/sierpinski.png?raw=true)

The [Hilbert Curve](http://en.wikipedia.org/wiki/Hilbert_curve):

![Hilbert Curve](images/hilbert.png?raw=true)

