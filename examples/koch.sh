#! /bin/sh

echo 'f--f--f' | ./lsystem.py -r 'f:f+f--f+f' -t 4 | ./lplot.py -a 60 -l 10 -f koch.png

