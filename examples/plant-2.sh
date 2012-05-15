#! /bin/sh

echo 'f' | ./lsystem.py -r 'f:f[-f]f[+f][f]' -t 5 | ./lplot.py -a 25 -l 10 -f plant-2.png

