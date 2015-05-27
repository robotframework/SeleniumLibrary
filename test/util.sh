#!/usr/bin/bash

#rename files to .robot
RES_FILES=`find . -name "*.txt" -print`

for f in $RES_FILES
do
   NAME=`echo $f | sed "s/\.txt/\.robot/g" -`
   #printf "%s %s\n" $f $NAME
   git mv $f $NAME
done

#fix resource.robot library name
RES_FILES=`grep -Rl "resource.robot" *`

for f in $RES_FILES
do
   sed -i "s/resource\.txt/resource\.robot/g" $f
done

