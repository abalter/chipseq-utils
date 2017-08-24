#!/bin/bash

main()
{
    peak_fasta_dir=$1
    kmer_file=$2
    output_file=$3

    echo "kmer    protein dna rep peak_start peak_stop chrom chrom_start chrom_stop" \
        > $output_file

    for fasta in $(ls $peak_fasta_dir/*.fasta); do
        for kmer in $(cat $kmer_file)
            # get treatment
            getTreatment $fasta
            # get  

}

getTreatment()
{
    echo "getting treatment"
    local filename=$1
    echo "filename: $filename"
    treatment_string=$(echo $filename | cut -d"-" -f1)
    echo "treatment_string: $treatment_string"
    treatment["protein"]=$(echo $treatment_string | cut -d"_" -f1)
    echo "protein: ${treatment["protein"]}"
    treatment["dna"]=$(echo $treatment_string | cut -d"_" -f2)
    echo "dna: ${treatment["dna"]}"
    treatment["rep"]=$(echo $treatment_string | cut -d"_" -f3)
    echo "rep: ${treatment["rep"]}"
}

############## Execute Main ###########
main "@"
######################################
