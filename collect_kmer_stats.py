#!/usr/bin/python

import os
import sys
import re

iglregex="DNA[a-zA-Z0-9]+_([a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+)_[a-zA-Z0-9_\.]+$"

kmers = []
barcodes = []

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
        sample_identifier_regex="",
        fastqc_directory="",
        output_directory="",
    ):

    sample_identifier_regex = iglregex

    print(fastqc_directory)
    print(sample_identifier_regex)

    fastqc_directories = [dir for dir in os.listdir(fastqc_directory) if dir.endswith("_fastqc") ]
    print(fastqc_directories)
    print(len(fastqc_directories))
    #exit()

    #sys.exit()

    for dirname in fastqc_directories:
        print("dir: " + fastqc_directory + "/" + dirname)
        full_match = re.search(sample_identifier_regex, dirname)
        if full_match:
            barcode = full_match.group(1)
            print("matched barcode: " + barcode);
            data_file_path = fastqc_directory + "/" +  dirname + "/fastqc_data.txt"
            collectKmerDataForSample(data_file_path, barcode)
        else:
            print("unmatched file " + dirname)
            barcode = "unmatched"
       
    #barcodes.sort()
    #kmers.sort()
    writeDataToTables()

def collectKmerDataForSample(data_file_path, barcode):
    line_data = []
    kmer = ""
    temp_kmer_stats = {}
    # if barcode is not in list then add to list
    # and make placeholder in all_kmer_data
    if barcode not in barcodes:
        barcodes.append(barcode)
        all_kmer_data[barcode] = {}

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
    #print("skipping header line")
    fastqc_summary.readline()
    
    #read until end of module
    print("reading kmer data")
    line = fastqc_summary.readline()
    while line.find(">>END_MODULE") == -1:
        #print(line)
        line_data = re.split("[\t\n]", line)
        print('length ' + str(len(line_data)))
        print(line_data)
        kmer = line_data[0]
        # add kmer if not already in list
        if kmer not in kmers:
            print("new kmer: " + kmer)
            kmers.append(kmer)
        temp_kmer_stats = \
        {
            "count": line_data[1],
            "p_value": line_data[2],
            "obs_exp_max": line_data[3],
            "max_obs_exp_position": line_data[4]
        }
        all_kmer_data[barcode][kmer] = temp_kmer_stats
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
   #                 all_kmer_data[barcode][kmer] = temp_kmer_stats
    
    return all_kmer_data

def writeDataToTables():
    print("writing data")
    header_line = "barcode, " + ", ".join(kmers) + "\n"
    for table in stats_tables:
        print("table: " + table)
        with open(table + ".csv", 'w') as table_file:
            table_file.write(header_line)
            for barcode in barcodes:
                line_array = []
                line_string = ""
                #print("sequencID: " + barcode)
                line_array.append(barcode)
                these_kmers = all_kmer_data[barcode].keys()
                for kmer in kmers:
                    #print("kmer: " + kmer)
                    if kmer in these_kmers:
                        line_array.append \
                        (
                            all_kmer_data[barcode][kmer][table]
                        )
                    else:
                        line_array.append("0")

                line_string = ", ".join(line_array) + "\n"
                #print(line_string)
                table_file.write(line_string)
        
        
if __name__ == "__main__":
    args = sys.argv
    print(args[1])
    print(args[2])
    print(args[3])
    
    sample_identifier_regex = args[1]
    fastqc_directory = args[2]
    if args[3] == "":
        output_directory = fastqc_directory
    else:
        output_directory = args[3]

    print("sample_identifier_regex", sample_identifier_regex)
    print("fastqc_directory", fastqc_directory)
    print("output_directory", output_directory)

    main(
        sample_identifier_regex=sample_identifier_regex,
        fastqc_directory=fastqc_directory,
        output_directory=output_directory,
    )




