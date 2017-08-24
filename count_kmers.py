#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

from collections import defaultdict
from itertools import islice
import sys
import re

sample_regex = "([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_kmer_counts_([0-9]+)$"
ref_regex = "([a-zA-Z0-9_]+)_kmer_counts_([0-9]+)\.[a-zA-Z0-9]+$"
igl_regex = "((DNA[a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_([a-zA-Z0-9_]+))$"

#-------------------------- countKmers ----------------------#
def countKmers(
        samplefile="",
        kmer_length=0
    ):

    #kmer_counts = {''.join(p):0 for p in product(bases, repeat=kmer_length)}

    print("in countKmers")
    print("samplefile: " + samplefile)
    
    kmer_regex = "[ACGT]{" + str(kmer_length) + "}"

    kmer_counts = defaultdict(int)

    ### read through the samplefile
    with open(samplefile) as f:
        ### use itertools islice to read every 4th line 
        for line in islice(f, 1, None, 4):
            for n in range(len(line) - kmer_length + 1):
                kmer = line[n:n+kmer_length]
                # make sure there is at least one k-mer
                if re.search(kmer_regex, kmer):                 
                    ### get the kmer from the first k characters
                    kmer_counts[kmer] += 1
                else:
                    continue
            
   #print("kmer_counts")
   #print(kmer_counts)
    
    ### return kmer counts
    return kmer_counts
#----------------------------------------------#


#---------  printKmerCounts -------------#
def printKmerCounts(kmer_counts={}, outfile=None):
    
    for kmer, count in kmer_counts.items():
        print("{}\t{}".format(kmer, count),file=outfile)

#---------------------------------------------#


#--------- printNormalizedKmerCounts -------------###
def printNormalizedKmerCounts(sample_kmer_counts={}, ref_countfile="", outfile=None):
    
    ref_kmer_counts = getRefCounts(ref_countfile=ref_countfile)

    for kmer, count in kmer_counts.items():
        print(
            "{}\t{}\t{}"
            .format(kmer, count, count/int(ref_kmer_counts[kmer])), 
            file=outfile
            )

#---------------------------------------------#


#--------- getRefCounts ----------------------#            
def getRefCounts(ref_countfile=""):
    with open(ref_countfile) as f:
        ref_kmer_counts = dict([line.split() for line in f])

    #print(ref_kmer_counts)
    return ref_kmer_counts



#--------- getFileParts  ----------------#
def getFileParts(filename):
    import os.path as path
    c
    path, filename = path.split(filename)
    if "." in filename:
        filename, ext = filename.rsplit(".", 1)
    else:
        ext = ""
   
    return path, filename, ext
#----------------------------------------------#


#-------- main --------------------------------#
if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description='Count kmers in fastq files',
        epilog="""Tip: You can use this to create your reference. For instance
            run on your reference geneome without the --reference (-r)
            flag"""
        )
    parser.add_argument('--sample', '-s', 
        required=True, 
        type=str, 
        help="The sample fastq file"
        )
    parser.add_argument('--outfile', '-o', 
        required=False, 
        type=str, 
        help="output file",
        default=None
        )
    parser.add_argument('--kmer-length', '-k',
        required=True, 
        type=int, 
        help="kmer length"
        )
    parser.add_argument('--reference', '-r', 
        required=False, 
        type=str, 
        help="reference kmer count file for normalized counts",
        default=None
        )
    
    args = parser.parse_args()

    #sys.exit()

    sample = args.sample
    outfilename = args.outfile
    kmer_length = args.kmer_length
    ref_countfile = args.reference

    #print("sample " + sample)
    #print("kmer_length " + str(kmer_length))

    ### Count kmers
    kmer_counts = countKmers(
        samplefile=sample,
        kmer_length=kmer_length
    )
   
    ### create outfile object or leave as None
    if outfilename != None:
        outfile = open(outfilename, 'w')
    else:
        print("No outfile specified. Writing to stdout.")

    if ref_countfile == None:
        print("Did not get a reference file. Not normalizing.")
        printKmerCounts(
            sample_kmer_counts=kmer_counts, 
            outfile=outfile
        )
    else:
        print("Got reference file " + ref_countfile + ". Normalizing")
        printNormalizedKmerCounts(
            sample_kmer_counts=kmer_counts, 
            ref_countfile=ref_countfile,
            outfile=outfile
        )




