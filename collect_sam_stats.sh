source_directory=$1
studyid=$2
output_file=${studyid}_stats.txt
output_directory=$3

echo "source directory: $source_directory"
echo "studyid: $studyid"
echo "ouput_file: $output_file"
echo "output_directory: $output_directory"

if [ -e $output_directory/$output_file ]; then
    rm $output_directory/$output_file
fi

touch $output_directory/$output_file

#first_file=$(ls $source_directory | egrep "[ACGT]{7,}_stats.txt" | head -1)
first_file=$(ls $source_directory | head -1)
echo "first_file"
echo $first_file

#exit

#column_headings=cat $first_file | grep '^SN' | sed 's/\t/ /g' | tr -s ' ' | cut -d' ' -f2 | awk -F '[:#]' '{ print $1 }' | tr '\n' ', ' | sed 's/ ,/,/g')

# grep '^SN' -- lines beginning with SN
# sed 's/\t/ /g' -- change tabs to spaces
# tr -s ' ' -- squeeze spaces (necessary?)
# cut -d' ' -f2 -- get the 2nd column, which has the field name 
# awk -F '[:#]' '{ print $1 } -- strip the ":"


# awk '{print $1,F,$2,F,F,$3,$4,$5,"Tom"}' FS=, OFS=, F='NULL' file
# http://stackoverflow.com/questions/19220493/add-columns-with-default-values-into-csv-file
# get sam fields

echo ${source_directory}/${first_file}
field_list=$( cat ${source_directory}/${first_file} | grep "^SN" | awk -F"\t" '{print $2}' | tr ":" "," )
#echo "field list:"
#echo -e ${field_list}
echo $field_list | tr "," "\n"

#for f in ${field_list} | tr "," "\n"
#do
#    echo $f
#done

column_headings="fileid, $field_list"
#echo $column_headings | sed -e "s/, /\n/g"


#echo "column headings"
#for i in $column_headings | sed -e "s/,/\n/g"
#do
#    echo $i
#done

#exit

echo $column_headings > ${output_directory}/${output_file}
#exit

for filename in $(ls $source_directory)
do
    filepath=$source_directory/$filename
    echo "filename: $filename"
    fileid=$(echo $filename | sed -E -n "s/([a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+)-[a-zA-Z0-9_\.]+/\1/p")
    echo "fileid: $fileid"
    stats=$(cat $filepath |  grep '^SN' | sed 's/\t/ /g' | tr -s ' ' | cut -d' ' -f2- | awk -F '[:#]' '{ print $2 }' | tr '\n' ', ' | sed 's/ ,/,/g')
    #stats=$(cat $filename |  grep '^SN' | sed 's/\t/ /g' | tr -s ' ' | cut -d' ' -f2- | awk -F '[:#]' '{ print $2 }' | tr '\n' ', ')
    echo $fileid, ${stats%%,}
    echo $fileid, ${stats%%,} >> ${output_directory}/${output_file}
done
