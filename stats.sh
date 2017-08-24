#!/bin/bash

BIN_DIR=somepath/bin

infile=$1
filename=$(basename $infile)
filename=${filename%%.*}
outdir=$2
outfile=${filename}_stats.txt

echo "infile: $infile"
echo "filename: $filename"
echo "outfile: $outfile"
echo "$BIN_DIR/samtools stats infile > $outdir/$outfile"
$BIN_DIR/samtools stats $infile > $outdir/$outfile
