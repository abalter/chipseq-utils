#!/bin/bash

REF_GENOME_DIR="somepath/genomic_resources/genomes/mm10/release-85"
REF_GENOME="$REF_GENOME_DIR/Mus_musculus.GRCm38.dna.primary_assembly.fastq"

for i in $(seq 5 10); do
    echo "counting $i-mers"
    cmd="time perl count_kmers.pl $REF_GENOME . $i"
    echo $cmd
    echo 
done


