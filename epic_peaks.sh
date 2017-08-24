#!/bin/bash

echo "command line:"
echo "$@"

source activate epic

treated=$1
control=$2
shortname=$3
results=$4

echo "treated_bam: $treated"
echo "control_bam: $control"
echo "shortname: $shortname"
echo "results_directory: ${results}"

outfile=${results}/${shortname}_peaks.bed
echo "outfile: $outfile"


### Temporarily commenting out checks to test with multiple
### Chip and input files
<<comment
if [[ ! -e $treated ]]; then
    echo "treated bedfile $treated not found"
    exit
fi

if [[ ! -e $control ]]; then
    echo "control bedfile $control not found"
    exit
fi
comment

cmd="
epic                        \
    --treatment $treated    \
    --control $control      \
    --genome hg38           \
    --window-size 50        \
    --fragment-size 300     \
    --keep-duplicates       \
"

echo $cmd

echo "about to execute epic command"
### The awk command does four thigns:
# 1) keeps the first line header that epic makes with the command issued
# 2) converts spaces to tabs
# 3) comments out the header line
# 4) removes "chr" from the chromosome numbers, i.e. "chr1" --> "1"
eval $cmd \
| awk 'NR==1{print $0}NR>2{gsub(/^chr/, ""); gsub(/ /, "\t"); print $0}NR==2{gsub(/ /, "\t");print "# "$0}' \
| bedtools sort -header -i - \
> $outfile

echo "done executing epic command"

if [[ "$?" != 0 ]]
then
    printf "error with peaks \n\n"
    exit
else
    printf "peak calling completed \n\n"
fi
