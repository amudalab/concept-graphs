#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1

for transcript in $transcript_list; do 
	python -m features.dispersion $transcript
done

