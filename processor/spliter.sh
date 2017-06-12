#!/bin/sh
for f in /results/*-result.csv ;
do
   echo 'Processing: ' $f
   cut -f2 -d',' $f > $f.creation
   cut -f3 -d',' $f > $f.bytarget
   cut -f4 -d',' $f > $f.bybody
done