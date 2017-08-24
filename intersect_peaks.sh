#!/bin/bash

treatment=$1
chip=$2
replicates=$3
file_tag=$4
peaksdir=$5
outdir=$6

main ()
{
    if [[ $1 == "help" ]]; then
        echo "[treatment] [chip] [\"rep1 rep2 ...\"] [file tag e.g. _peaks.bed] [peaks directory] [output directory]"
        exit
    fi

    firstrep=${replicates#* }
    otherreps=${replicates%% *}
    reparray=($replicates)
    num_reps=${#reparray[@]}

    outfile 
    
    argline="intersect -a "
    argline="$argline ${peaksdir}/${treatment}_${chip}_${firstrep}_${file_tag} -b"
    for rep in otherreps; do
        argline="$argline ${peaksdir}/${treatment}_${chip}_${rep}_${file_tag}"
    done
    argline="$argline > $outdir"

    cmd="bedtools intersect $argline"
    echo $cmdasdfasdf
    #eval $cmd
}


cut -f1-3 a.bed | bedtools intersect -a - -b b.bed | paste - a.bed | paste - b.bed
