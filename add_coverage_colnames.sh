#!/bin/bash

basecolnames="chr   start   stop    peak_name   score   strand  fold_change -log10(pvalue)  -log10(qvalue)"

filename=$1

extra_colnames="${@:2}"
extra_colnames=$(echo $extra_colnames | tr -s " " | tr " " "\t")

#echo $extra_colnames

all_colnames="$basecolnames	$extra_colnames"
echo "$all_colnames"

sed -i "1i$all_colnames" $filename

