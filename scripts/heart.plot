set datafile separator ","
set autoscale fix
set key outside right center

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12

set xdata time

set timefmt "%s"
set format x "%d%H"

set style data fsteps

set ylabel "BPM"

set xtics nomirror
set xtics rotate

set title "Adam"

set terminal png size 1920,1080
set output 'heart.png'

plot '/tmp/heart.csv' using 1:2 w lp notitle

pause -1
