#!/bin/bash

BIN_DIR=somepath/bin

infile=$1
filename=$(basename $infile)
filename=${filename%%.*}
outdir=$2
outfile=${filename}_flagstat.txt

echo "infile: $infile"
echo "filename: $filename"
echo "outfile: $outfile"
echo "$BIN_DIR/samtools flagstat $infile > $outdir/$outfile"
$BIN_DIR/samtools flagstat $infile > $outdir/$outfile
