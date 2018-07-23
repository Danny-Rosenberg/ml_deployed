#!/usr/bin/env bash

echo "we're inside prediction wrapper"
echo "here's one:" $1
echo "here's two:" $2
echo "here's three:" $3


python raw_input_processor.py "$1" "$2" "$3"
