#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
ext=$2

for transcript in $transcript_list; do 
	python -m video.occurrence contiguous $transcript
done
