#!/bin/bash

treated=$1
control=$2
shortname=$3
results=$4

echo "treated_bam: $treated"
echo "control_bam: $control"
echo "treated_shortname: $shortname"
echo "results_directory: ${results}"

if [[ ! -e $treated ]]; then
    echo "treated bamfile $treated not found"
    exit
fi

if [[ ! -e $control ]]; then
    echo "control bamfile $control not found"
    exit
fi

#CONDA_BIN="somepath/miniconda2/bin"

#peaksfilename=$treated_shortname-peaks
#paramsfile=$treated_shortname-params.ouexit

#source activate macs

echo $(which macs2)

#exit

cmd="
macs2 callpeak \
    --treatment $treated \
    --control $control \
    --name $shortname \
    --outdir $results/peaks \
    --keep-dup all \
    --gsize hs \
    --broad \
    --bdg \
    --verbose 4
"

echo $cmd
eval $cmd

#source deactivate macs
#conda remove -y --name macs --all

if [ "$?" != 0 ]
then
    printf "error with peaks \n\n"
    exit
else
    printf "peak calling completed \n\n"
fi
