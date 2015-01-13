#!/usr/bin/bash

OLD_EXT="txt"
NEW_EXT="robot"

#Option -r reverts changes
if [ "$1" = "-r" ];
then
    OLD_EXT="robot"
    NEW_EXT="txt"
fi
#rename files from .$OLD_EXT to .$NEW_EXT
RES_FILES=`find . -name "*.$OLD_EXT" -print`

for f in $RES_FILES
do
   NAME=`echo $f | sed "s/\.$OLD_EXT/\.$NEW_EXT/g" -`
   #if not using git just change to: mv $f $NAME
   git mv $f $NAME
done

#fix resource.robot library name

RES_FILES=`grep -Rl "resource.$OLD_EXT" *`

for f in $RES_FILES
do
   sed -i "s/resource\.$OLD_EXT/resource\.$NEW_EXT/g" $f
done

