#!/bin/bash

fastqckmerfile=$1
countdir=$2
countfile=$3

echo "fastqckmerfile: $fastqckmerfile"
echo "countdir: $countdir"
echo "countfile: $countfile"

if [[ -e $countfile ]]; then
    echo "removing count file $countfile"
    rm $countfile
else
    echo "no count file: $countfile"
fi

regex="([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9_]+)\.[a-z]+$"

kmerlist=$(cat $fastqckmerfile | tr "\n" " ")

#echo $kmerlist

headerline="prot,chip,rep,"$(echo $kmerlist | tr " " ",")
echo $headerline
echo $headerline >> $countfile

for i in $(ls $countdir/*.tsv); do
    
    name=$(basename $i)

    $(echo $name | sed -E -n "s/$regex/ eval prefix=\1 prot=\2 chip=\3 rep=\4 suffix=\5 /p")

    echo "prefix: $prefix"
    echo "prot: $prot chip: $chip rep: $rep"
    echo "suffix: $suffix"
    
    line="$prot,$chip,$rep"
    
    for k in $kmerlist; do
        count=$(grep $k $i | cut -f2)
        #echo "$k: $count"
        line="$line,$count"
    done

    #echo $line
    echo $line  >> $countfile

done

