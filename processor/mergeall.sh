#!/bin/sh

for dir in /results/* ; 
do 
for n in 'mongo' 'neo' 'sql' ; 
do 
eval /app/merger.py $dir/$n 
done
done


