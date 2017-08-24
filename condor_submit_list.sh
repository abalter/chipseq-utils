#!/bin/bash

executable=$1
results_directory=$2
arguments_list=$3

# strip ending "/" if exists
exexecutable=$(echo "$executable" | sed -e 's/\/$//g')
results_directory=$(echo "$results_directory" | sed -e 's/\/$//g')

#tempbase=$(basename $executable)
#executable_name=${tempbase%.*i}
echo "executable: $executable"
echo "output directory: $results_directory"

if [ "$executable" == "help" ]; then
    printf "
    condor_submit executable results_directory executable [list of arguments]

    the list of argument is comprised of a comma separated list
    of arguments to the executable which could consist of flags
    and a filename.

    for instance, 
        condor_submit /bin/ ~/outputs ls    \"-lrt dir1,-lrt dir2,-lrt dir3\"

"
    exit 0

fi

if [ ! -d $results_directory ]; then
    echo "creating output directory $results_directory"
    mkdir -p $results_directory
fi

#if [ -e ${results_directory}/logs ]; then
#    echo "deleting old logs in output directory $results_directory"
#    rm -rf ${output_director}/logs/*
#else
#    echo "creating log directory"
#    mkdir $results_directory/logs
#fi

if [ ! -d ${results_directory}/logs ]; then
    echo "creating log directory"
    mkdir -p ${results_directory}/logs
else
    echo "deleting old log files"
    rm -rf ${results_directory}/logs/*.out
    rm -rf ${results_directory}/logs/*.err
    rm -rf ${results_directory}/logs/*.log
fi


request_cpus=8
request_memory=56GB
email=balter@ohsu.edu
getenv="True"
notification=Error

#submit_file=condor_qc_$timestamp.csf

timestamp=$(date +%F_%T)

printf "
initialdir              = $(pwd)
executable              = ${executable}
log                     = ${results_directory}/logs/\$(Cluster).\$(Process).log
output                  = ${results_directory}/logs/\$(Cluster).\$(Process).out
error                   = ${results_directory}/logs/\$(Cluster).\$(Process).err
request_cpus            = $request_cpus
request_memory          = $request_memory
notify_user             = $email
notification            = $notification
getenv                  = $getenv
should_transfer_files   = Yes

" > ${results_directory}/submit.csf

echo "arguments"
echo $arguments_list


while IFS='' read -r line || [[ -n "$line" ]]; do
    argline="arguments               = \"$line\""
    echo $argline
    echo $argline >> ${results_directory}/submit.csf
    echo "queue" >> ${results_directory}/submit.csf
    echo "" >> ${results_directory}/submit.csf
done < "$3"


<<comment
OIFS=$IFS;
IFS=",";

for arguments in $arguments_list; do
    #filename=$(echo argument | egrep -o "[a-zA-Z0-9]+$")
    #outut_filename=${filename}_${executable_name}.txt
    #echo $arguments
    #echo "arguments               = \"$arguments\"" 
    test="arguments               = \"$arguments\"" 
    echo $test
    echo $test >> ${results_directory}/submit.csf
    #echo "arguments               = \"$arguments\"" >> submit.csf 
    echo "queue" >> ${results_directory}/submit.csf
    echo "" >> ${results_directory}/submit.csf
done

IFS=$OIFS
comment

