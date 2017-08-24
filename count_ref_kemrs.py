#!/usr/bin/env python
import sys
from collections import defaultdict

def countKmers(filename, kmer_length):
    sequence= open(filename)
    counts = defaultdict(int)
    current_kmer = ""
    #print("filename: " + filename)
    #print("kmer_length: " + str(kmer_length))

    for k in range(kmer_length-1):
        #print("k: " + str(k))
        current_kmer += sequence.readline()[:-1].strip()
        #print(current_kmer)

    base = sequence.readline()
    while base:
        current_kmer += base[0]
        counts[current_kmer] += 1
        current_kmer = current_kmer[1:]
        base = sequence.readline().strip()

    for kmer in counts:
        print(kmer + "\t" +  str(counts[kmer]))

    sequence.close()

if __name__ == "__main__":
    kmer_length = int(sys.argv[1])
    filename = sys.argv[2]
    countKmers(filename, kmer_length)
