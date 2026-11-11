#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
inputfolder=$2
outputfolder=$3
ext=$4

for transcript in $transcript_list; do 
	python -m video.occurrence frequency $transcript
done
