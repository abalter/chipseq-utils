#!/bin/bash

source_directory=$1
file_extension=$2


### Executable Paths
BIN_DIR="somepath/bin"
PICARD="$BIN_DIR/picard/picard-tools-1.110"
GATK="$BIN_DIR/GATK-3.5.jar"

### Genome resources
REF_GENOME_DIR="somepath/genomic_resources/genomes/rat"
REF_GENOME="$REF_GENOME_DIR/Rattus_norvegicus.Rnor_6.0.dna.toplevel.fa"

echo "source directory: $source_directory"
echo "file_extension: $file_extension"

current_directory=$(pwd)
echo "current_directory: $current_directory"
cd $source_directory
echo $(ls *.${file_extension}) | tr " " "\n" > input.list

echo "input list"
cat input.list

#exit

java -jar $GATK \
`  `-T DepthOfCoverage \
`  `-R $REF_GENOME \
`  `-o depth.txt \
`  `-I input.list \
`  `--outputFormat csv

rm input.list

cd $current_directoryc
