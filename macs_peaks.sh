#!/bin/bash

echo "command line:"
echo "$@"

source activate p27

treated=$1
control=$2
shortname=$3
results=$4
results=${results%%/}

echo "treated_bam: $treated"
echo "control_bam: $control"
echo "shortname: $shortname"
echo "results_directory: ${results}"

outfile=${results}/${shortname}_peaks.bed
echo "outfile: $outfile"

#shortname=${treated%%.*}
#echo "shortname: $shortname"

cmd="
macs2 callpeak              \
    --treatment $treated    \
    --control $control      \
    --name $shortname       \
    --outdir $results       \
    --keep-dup all          \
    --gsize hs              \
    --broad                 \
    --bdg                   \
    --verbose 4
"



echo $cmd

eval $cmd
