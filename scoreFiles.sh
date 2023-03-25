#!/bin/bash

PRINT_HEADER="--header"
INPUT_FILE=$1
OUTPUT_FILE=$2

rm $OUTPUT_FILE

#while IFS=: read -r f1 f2 f3 f4 f5 f6 f7
while IFS=' ' read -r label filename
do
	if [ -n "$label" ]; then
		if ! [[ "$label" =~ ^#.*$ ]]; then
			printf 'Label: %s, File: %s\n' "$label" "$filename"
			python3 main.py "$label" "$filename" "$PRINT_HEADER" >> $OUTPUT_FILE
			PRINT_HEADER=
		fi
	fi
done <"$INPUT_FILE"

