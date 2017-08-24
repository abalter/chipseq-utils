#!/usr/bin/python

import os
import sys
import re


kmers = []
sequenceIDs = []

stats_tables = \
[
    "count",
    "p_value",
    "obs_exp_max",
    "max_obs_exp_position"
]

all_kmer_data = {}

#data_file_name = "fastqc_data.txt"

def main(
        fastqc_directory="",
        output_file="",
        sample_identifier_regex=""
    ):

    #print(fastqc_directory)
   # print(sample_identifier_regex)

    #print([d for d in os.listdir(fastqc_directory)])

    #sys.exit()

    for dir in [dir for dir in os.listdir(fastqc_directory) if dir.endswith("*_fastqc"):
    # for item in os.listdir(fastqc_directory):
        #print("item: " + item)
        item_path = os.path.join(fastqc_directory, item)
        if os.path.isdir(item_path):
            data_file_path = os.path.join(item_path, data_file_name)
            match = re.search(sample_identifier_regex, item)
            if match:
                sequenceID = match.group()
                collectKmerDataForSample(data_file_path, sequenceID)
            else:
                print("unmatched file " + item)
                sequenceID = "unmatched"
            print(data_file_path)
            #print("sequenceID: " + sequenceID)
    #sequenceIDs.sort()
    #kmers.sort()
    writeDataToTables()


def collectKmerDataForSample(data_file_path, sequenceID):
    line_data = []
    kmer = ""
    temp_kmer_stats = {}
    # if sequenceID is not in list then add to list
    # and make placeholder in all_kmer_data
    if sequenceID not in sequenceIDs:
        sequenceIDs.append(sequenceID)
        all_kmer_data[sequenceID] = {}

    #open summary file
    #raw_input("opening file " + data_file_path)
    #data_file_path = "testfile.txt"
    fastqc_summary = open(data_file_path, 'r')
    
    # read until kmer section
    line = fastqc_summary.readline()
    while line.find(">>Kmer") == -1:
        #raw_input("reading line")
        line = fastqc_summary.readline()
        #raw_input("printing line")
        #print(line)

    #raw_input("found kmer section")
    
    # skip header line
    print("skipping header line")
    fastqc_summary.readline()
    
    #read until end of module
    print("reading kmer data")
    line = fastqc_summary.readline()
    while line.find(">>END_MODULE") == -1:
        print(line)
        line_data = re.split("[\t\n]", line)
        print(line_data)
        kmer = line_data[0]
        # add kmer if not already in list
        if kmer not in kmers:
            kmers.append(kmer)
        temp_kmer_stats = \
        {
            "count": line_data[1],
            "p_value": line_data[2],
            "obs_exp_max": line_data[3],
            "max_obs_exp_position": line_data[4]
        }
        all_kmer_data[sequenceID][kmer] = temp_kmer_stats
        # read next line
        line = fastqc_summary.readline()
    
    fastqc_summary.close()

   # with open(data_file_path) as data_file:
   #     ### read until kmer content
   #     for line in data_file:
   #         print(line)
   #         if line.find(">>Kmer") != -1:
   #             print("in kmer section")
   #             if line[0] == "#":
   #                 pass
   #             elif line.find(">>END_MODULE") != -1:
   #                 break
   #             else
   #                 #print(line)
   #                 line_data = line.split(",")
   #                 print(line_data)
   #                 break
   #                 kmer = line_data[0]
   #                 kmers.append(kmer)
   #                 temp_kmer_stats = \
   #                 {
   #                     "count": line_data[1],
   #                     "dfp_value": line_data[2],
   #                     "obs_exp_max": line_data[3],
   #                     "max_obs_epx_position": line_data[4]
   #                 }
   #                 all_kmer_data[sequenceID][kmer] = temp_kmer_stats
    
    return all_kmer_data

def writeDataToTables():
    print("writing data")
    header_line = "sequenceID, " + ", ".join(kmers)
    for table in stats_tables:
        print("table: " + table)
        with open(table + ".csv", 'w') as table_file:
            table_file.write(header_line)
            for sequenceID in sequenceIDs:
                line_array = []
                line_string = ""
                #print("sequencID: " + sequenceID)
                line_array.append(sequenceID)
                these_kmers = all_kmer_data[sequenceID].keys()
                for kmer in kmers:
                    #print("kmer: " + kmer)
                    if kmer in these_kmers:
                        line_array.append \
                        (
                            all_kmer_data[sequenceID][kmer][table]
                        )
                    else:
                        line_array.append("-999")

                line_string = ", ".join(line_array) + "\n"
                #print(line_string)
                table_file.write(line_string)
        
        
if __name__ == "__main__":
    args = sys.argv
    #print(args[1])
    #print(args[2])
    
    if args[3] != "":
        output_directory = args[3]
    else
        output_directory = args[2]

    main(
        fastqc_directory=args[2],
        output_directory=output_directory,
        sample_identifier_regex=args[1],
    )





