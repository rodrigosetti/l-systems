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

What is this Project?
---------------------

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
