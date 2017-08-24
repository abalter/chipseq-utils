#!/bin/bash

refkmercounts=$1
samplekmercounts=$2
outdir=$3
k=$4 # intended k-mer length

echo "samplekmercounts: $samplekmercounts"
echo "refkmercounts: $refkmercounts"
echo "outdir: $outdir"

samplename=$(basename $samplekmercounts)
refname=$(basename $refkmercounts)
echo "samplename: $samplename"
echo "refname: $refname"

sample_regex="([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_kmer_counts_([0-9]+)\.tsv$"
ref_regex="([a-zA-Z0-9_]+)_kmer_counts_([0-9]+)\.[a-zA-Z0-9]+$"
echo $sample_regex
echo $ref_regex
$(echo $samplename | sed -E -n "s/$sample_regex/eval prot=\1 chip=\2 rep=\3 kmer_length=\4 /p")
$(echo $refname | sed -E -n "s/$ref_regex/eval genome=\1 kmer_length=\2 /p")

echo "prot: $prot chip: $chip rep: $rep"
echo "genome: $genome kmer_length: $kmer_length"


if [[ $k != $kmer_length ]]; then
    echo "the assumed kmer length does not seem to match the filename"
    echo "will not proceed"
    exit
fi

outfile=${prot}_${chip}_${rep}_normalize_kmer_count_${kmer_length}.tsv
echo "outfile: $outfile"

n=0
while IFS='' read -r line || [[ -n "$line" ]]; do
    #echo $line
    $( 
    echo $line |
        tr " " "-" | 
        sed -E -n "s/([ACGT]+)-([0-9]+)/eval kmer=\1 refcount=\2/p" 
    )
    #echo "kmer: $kmer refcount: $refcount"
    samplecount=$(grep $kmer $samplekmercounts | cut -f2)
    #echo "samplecount: $samplecount"
    normalizedcount=$(perl -e "print $samplecount/$refcount")
    #echo "normalizedcount: $normalizedcount"
    printf "$kmer\t$samplecount\t$normalizedcount\n" >> temp
 done < $refkmercounts

 mv temp $samplekmercounts

