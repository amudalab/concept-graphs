#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
transcript_list=$1

echo "tfidf Generation"
echo $transcript_list
echo "After replecement"
transcript_list_new={$transcript_list// /,}

python -m features.tfidf "Porter-Stemmer" 4 $transcript_list_new
echo "done"

