#!/bin/bash

### Main
main()
{
    echo "In main"
    echo "Command:  $0 $@"

    processArguments "$@"

    numbamfiles=$(echo $bamfiles | wc -w)
    bamfilearray=($bamfiles)
    

    if [[ "$outfile" == "" ]]; then
        echo "no outfile, writing to stdout"
        bedtools multicov -bams $bamfiles -bed $bedfile | awk -v numbamfiles=$numbamfiles '\
            BEGIN {
                
                half=numbamfiles/2}
            }
            {

        
        intersectBed -wb -a $bedfile1 -b $bedfile2 | cut -f1-5,9-
        #bedtools intersect -wb -a $bedfile1 -b $bedfile2 | bedtools intersect -wb -b $bedfile1 -a - 
    else
        echo "writing to outfile: $outfile"
        intersectBed -wb -a $bedfile1 -b $bedfile2 | cut -f1-5,9- >> $outfile
        #bedtools intersect -wb -a $bedfile1 -b $bedfile2 | bedtools intersect -wb -b $bedfile1 -a - >> $outfile
    fi
}

### Process Arguments
processArguments()
{
    
    echo "Passed to processArguments: $0 $@"

    # Initialize our own variables:
    keep_header="false"
    bedfiles=""
    outfile=""

    while getopts "hkb:o:" opt; do
        case $opt in
            h | --help )
                echo "help"
                showHelp
                exit 0
                ;;
            k | --keep-header )
                #echo "keep header"
                keep_header="true"
                ;;
            b | --bed )
                #echo "got bedfile $OPTARG"
                bedfiles="$bedfiles $OPTARG"
                ;;
            o | --outfile )
                outfile=$OPTARG
                echo "outfile: $outfile"
                ;;
            *)
                showHelp >&2
                exit 1
                ;;
        esac
    done


    echo "bedfiles: $bedfiles"
    echo "outfile: $outfile"
    echo "keep_header: $keep_header"
}


### Usage info
showHelp() 
{
cat << EOF
Usage: ${0##*/} [-h] [-k] -b BEDFILE_1 -b BEDFILE_2 [-b BEDFILE_3] ... [-o OUTFILE] 

**NOTE: longoptions are not currenlty implemented.**
**NOTE: currenlty handles only 2 bedfiles.**

Combines two bed files using the  \`bedtools intersect\` method to produce
a file with the follwing:
    1) The first three columns are the coordinates of the intersection.
    2) The next N columns are the full N columns of bedfile 1 (whatever N happens to be).
    3) The last M columns are the full M columns of bedfile 2.
    4) If the \`--keep-header\` flag is set, any columns at the top of the file beginning 
    with a "#" are assumed to be commented header information. These are preserved 
    for each file

    -h, --help      Display this help and exit
    -k, --keep-header
                    A flag to designate keeping the headers
    -b, --bed       A bed file to intersect. Currently only two accepted.
    -o, --outfile    The output file, or stdout.
EOF
}

### getHeader 
getHeader()
{
    echo "in get header"
    local file=$1
    #awk -v OFS="\t" '{if ($1~/^#/) {print $0"\n"} else {exit}}' $file > header_${tag}
    header=$(head -1 $file | tr -s " " | tr " " "\t")
}

main "$@"

exit 0
