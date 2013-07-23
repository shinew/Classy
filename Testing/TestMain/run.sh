#!/bin/bash

out_file=output.txt
ids=`cat allIDs | sed -n '101, 200 p'`
for id in $ids
do
#	echo $id
	python testProgram.py $id >> $out_file
	echo Done $id...
done
