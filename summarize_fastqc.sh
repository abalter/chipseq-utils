#!/bin/bash

fastqcdir=$1
outdir=$2
fastqcdir=${fastqcdir%%\/}
outdir=${outdir%%\/}
echo "processing fastqc results in $fastqcdir"
echo "summary in $outdir/fastqcsummary.csv"
#ls $fastqcdir

if [ -e "$outdir/fastqcsummary.csv" ]; then
    echo "old file exists"
    rm $outdir/fastqcsummary.csv
fi

regex="((DNA[a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9_]+))$"

header=""

for i in $(ls -d $fastqcdir/*.zip); do
    # Need to reset fullmatch or it just keeps the 
    # last value when the regex fails to find a new match.
    fullmatch=""
    #echo $i
    name=$(basename $i)
    name=${name%%.*}
    #echo "name: $name"
    #echo "header: $hddeader"
    
    ### parse the sample treatment details from file name
    ### assumes OHSU IGL format
    $(
        echo $name | sed -E -n "s/${regex}/ eval    \
            fullmatch=\1                            \
            prefix=\2                               \
            prot=\3                                 \
            chip=\4                                 \
            rep=\5                                  \
            suffix=\6                               \
            /p"                                     
    )
    echo "fullmatch: $fullmatch"

    if [ "$fullmatch" != "" ]; then
        echo "prefix: $prefix prot: $prot chip: $chip rep: $rep suffix: $suffix"
        #echo "unzip -c $i $name/summary.txt"
        
        ### capture the summary file to temp
        #echo " 
        #unzip -c $i $name/summary.txt                           \
        #    | tail -n +3   `# skip first two lines`             \
        #    | head -n -1   `# skip last line`                   \
        #    > temp         `# send to temp file--remove later`  \
        #"

        unzip -c $i $name/summary.txt                           \
            | tail -n +3   `# skip first two lines`             \
            | head -n -1   `# skip last line`                   \
            > temp         `# send to temp file--remove later`  
        #echo "catting temp"
        #cat temp

        ### write the header if not already done
        if [ "$header" == "" ]; then
            echo "writing header" 
            header=$(cat temp                                           \
                | cut -f2            `# 2nd column has name of stat`    \
                | tr "\n" ","        `# convert newlines to commas`     \
                | sed -e "s/,$//g"   `# remove the trailing comma`      \
                )
            header="prot,chip,rep,$header"
            
            echo "header:"
            echo $header
            echo $header >> $outdir/fastqcsummary.csv
        fi

        ### Collect the results
        results=$(cat temp                                          \
            | cut -f1            `# 1st column has results`         \
            | tr "\n" ","        `# convert newlines to commas`     \
            | sed -e "s/,$//g"   `# remove the trailing comma`      \
            )
            
        results="$prot,$chip,$rep,$results"
        
        echo "writing data: "
        echo $results
        echo ""
        
        echo $results >> $outdir/fastqcsummary.csv

    fi
done

rm temp

exit 0

