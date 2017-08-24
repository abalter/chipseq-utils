expath=$1
kmer_length=$2

outdir=results/kmer_counts_${kmer_length}
mkdir -p $outdir

for i in $(ls $(pwd)/raw/DNA*.fastq); do
    echo $i
    time perl $expath/count_kmers.pl \
        $i \
        $outdir \
        $kmer_length 
done

