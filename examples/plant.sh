#! /bin/sh

echo 'X' | ./lsystem.py -r 'X:f-[[X]+X]+f[+fX]-X' -r 'f:ff' -t 6 | ./lplot.py -a 25 -l 10 -f plant.png

