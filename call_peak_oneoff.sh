#!/bin/bash

datadir=$1
datadir=${datadir%%/}
prot=$2
chip=$3
rep=$4

echo "prot: $prot chip: $chip rep: $rep"

here=$(pwd)
echo $here

echo "datadir: $datadir"

#regex="((DNA[a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9i\._]+))"

regex="(([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)-[a-zA-Z0-9]+.bam)"

treated=$datadir/${prot}_${chip}_${rep}.bam
control=$datadir/${prot}_input_${rep}.bam
echo "treated: $treated"
echo "control: $control"
shortname=${prot}_${chip}_${rep}
echo "shortname: $shortname"

cmd="
macs2 callpeak \
    --treatment $treated \
    --control $control \
    --name $shortname \
    --outdir $here/results/peaks
    --keep-dup all \
    --gsize hs \
    --broad \
    --bdg \
    --verbose 4
"

echo $cmd

eval $cmd
