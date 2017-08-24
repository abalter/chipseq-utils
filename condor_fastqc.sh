#! /bin/bash

BIN_DIR="somepath/bin"

run_type=$1
data_directory=${2%/}
file_extension=$3
project_directory=${4%/}
results_directory=${5%/}

if [ $run_type == "help" ]; then
    printf "\
    run_type=\$1\n\
    data_directory=\$2\n\
    file_extension=\$3\n\
    project_directory=\$4\n\
    results_directory=\$5\n\
    \n\
    "
    exit
fi

printf "\
    run_type=$run_type\n\
    data_directory=$data_directory\n\
    file_extension=$file_extension
    project_directory=$project_directory\n\
    results_directory=$results_directory\n\
    \n\
    "

timestamp=$(date | sed 's/ /_/g' | sed 's/\:/-/g')
output_directory=$results_directory/QC_$timestamp
echo "output directory: $output_directory"

mkdir -p $output_directory
mkdir -p $output_directory/logs

common_dir=$project_directory
request_cpus=20
request_memory=56GB
email=balter@ohsu.edu
getenv="True"
notification=Error
max_execution_time=10000 

submit_file=condor_qc_$timestamp.csf

printf "
executable                  ="${BIN_DIR}/fastqc"
output                      =$output_directory/logs/\$(Cluster).\$(Process).out
error                       =$output_directory/logs/\$(Cluster).\$(Process).err
log                         =$output_directory/logs/\$(Cluster).\$(Process).log
request_cpus                =$request_cpus
request_memory              =$request_memory
notify_user                 =$email
notification                =$notification
getenv                      =$getenv
+MaxExecutionTime           =$max_execution_time

" \
> ${submit_file}

#for fasta_file in $(ls $data_directory *.fq.gz)
#for fasta_file in $(find data/fasta_files/ -type f -name "*.fq.gz" -exec basename {} \;

for fasta_file in $(ls $data_directory/*.${file_extension})
do
#	echo $(basename $fasta_file)
	argline="\
arguments                   =$fasta_file --outdir=$output_directory --extract --kmers=10"
	printf "$argline\nqueue 1\n\n" >> ${submit_file}
done

if [ $run_type == "test" ]; then
    cat $submit_file
    rm $submit_file
elif [ $run_type == "go" ]; then
    echo "moving submit file"
    echo "$sumbit_file"
    echo "to output directory"
    echo "$ouput_directory"
    mv $submit_file $output_directory

    condor_submit $output_directory/$submit_file
fi

