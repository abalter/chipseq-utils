#!/bin/awk -f


function calcFoldChange(line, numbamfiles, numfields, repnum)
{
    
}

BEGIN \
{
    numbamfiles = ARGC - 2;
    #printf "numbamfiles: %d\n", numbamfiles;
    half = numbamfiles/2;
    for (i = 2 ; i < ARGC + 1; i++)
    {
        #printf "%s\t", ARGV[i];
    }

    #print;
    #print "end of begin";
}
{
    if (NR==1)
    {
        #print "making the header";
        numfields = NF;
        #print NF, " Fields";
        # Initial header fields
        printf "#chr\tstart\tstop\t";

        # Header place holders
        for (i = 4 ; i < NF - numbamfiles ; i++)
        {
            printf "\t";
        }

        # Headers for samples
        for (i = 2 ; i < 2 + numbamfiles ; i++)
        {
            printf "%s\t", ARGV[i];
        }

        # Headers for fold changes
        printf "data/control\t";
        printf "control/data\t";
        printf "\n";

    }

    start = NF - numbamfiles + 1;
    end = start + half - 1;

    #printf "start: %d end: %d\n", start, end;

    A = 0;
    for (i = start ; i < end + 1 ; i++)
    {
        A += $i;
    }
    A = (A==0) ? 1: A;

    #printf "A: %d\n", A;

    start = end + 1;
    end = start + half - 1;

    #printf " start: %d end: %d\n", start, end

    B=0;
    for (i = start ; i < end + 1 ; i++)
    {
        B += $i;
    }
    B = (B==0) ? 1: B;

    #printf "B: %d\n", B;

    fold1 = A/B
    fold2 = B/A

    print $0"\t"fold1"\t"fold2

    ARGC = 1;   
}
END \
{
    #print "done";
}

