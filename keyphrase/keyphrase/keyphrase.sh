mode=$1
transcript_name=$2
stemmer_name=$3
pos_status=$4
pos_filter_file=$5
max_gram=$6
status="disable"

if [ "$mode" == "av" ] || [ "$mode" == "a" ]
then
	echo "Pre-Processing Audio Transcript"
	python pos.py $transcript_name $stemmer_name $pos_status
	if [ "$pos_status" == "enable" ] 
	then
		python grams_pos.py $transcript_name $max_gram $pos_filter_file $stemmer_name
	else
		python grams.py $transcript_name $max_gram $stemmer_name
	fi
	echo "Done -- Pre-Processing Audio Transcript"
fi

if [ "$mode" == "av" ] || [ "$mode" == "v" ]
then
	echo "Pre-Processing Text Area of Video"
	python text_stem.py $transcript_name $stemmer_name
	python extractgrams.py $transcript_name $max_gram
	echo "Done - Pre-Processing Text Area of Video"
fi

feature_list=$7
feature_ext=""
comma_str=","
export IFS=","

if [ "$mode" == "av" ] || [ "$mode" == "a" ] || [ "$mode" == "v" ]
then
	for feature in $feature_list; do
	  if [ "$feature" == "cscore" ] &&  [ "$mode" == "a" -o "$mode" == "av" ]
	  then
		echo "Cscore"
		python audio_features/cscore.py $transcript_name $stemmer_name
		ext="_cscore.txt"
		feature_ext=${feature_ext}${ext}${comma_str}
	  fi
	  if [ "$feature" == "localspan" ] &&  [ "$mode" == "a" -o "$mode" == "av" ]
	  then
		echo "Localspan"
		python audio_features/localspan.py $transcript_name $stemmer_name $max_gram
		ext="_localspan.txt"
		feature_ext=${feature_ext}${ext}${comma_str}
	  fi
	  if [ "$feature" == "cuewords" ] &&  [ "$mode" == "a" -o "$mode" == "av" ]
	  then
		echo "Cuewords"
		python audio_features/cue.py $transcript_name $stemmer_name $max_gram
		ext="_cue.txt"
		feature_ext=${feature_ext}${ext}${comma_str}
	  fi
	  if [ "$feature" == "tfidf" ] &&  [ "$mode" == "a" -o "$mode" == "av" ]
	  then
		echo "TF-IDF"
		python audio_features/tfidf.py $stemmer_name $max_gram $transcript_name
		ext="_tfidf.txt"
		feature_ext=${feature_ext}${ext}${comma_str}
	  fi
	  if [ "$feature" == "dispersion" ] &&  [ "$mode" == "a" -o "$mode" == "av" ]
	  then
		echo "Dispersion"
		python audio_features/dispersion.py $transcript_name $max_gram $stemmer_name
		ext="_disp.txt"
		feature_ext=${feature_ext}${ext}${comma_str}
	  fi
	  if [ "$feature" == "cont_ratio" ] &&  [ "$mode" == "v" -o "$mode" == "av" ]
	  then
		echo "Contiguous_Occurance_Ratio"
		ext="_cont.txt"
		python video_features/contiguous_count_ratio.py $transcript_name $ext
		feature_ext=${feature_ext}${ext}${comma_str}
	  fi
	 if [ "$feature" == "freq_ratio" ] &&  [ "$mode" == "v" -o "$mode" == "av" ]
	  then
		echo "Frequency Occurance Ratio"
		ext="_freq.txt"
		python video_features/freq_occur_ratio.py $transcript_name $ext
		feature_ext=${feature_ext}${ext}${comma_str}
	  fi
	done
fi
feature_ext="'"${feature_ext}"'"

export IFS=" "

echo "Integrating all feature results"
str="python write.py "$transcript_name" "$feature_list" "$feature_ext" "$stemmer_name
python write.py $transcript_name $feature_list $feature_ext $stemmer_name
#echo "$str"
train_file=$8
echo "Performing Machine Learning"
python ml_audio/Naive-Bayes/Naive-Bayes.py $train_file $transcript_name

