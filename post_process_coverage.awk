#!/bin/awk -f

BEGIN{
    OFS="\t";
    printf("#chr\tstart\tstop\tlog2_fold");
    for (i=1 ; i < ARGC-1 ; i++)
    {
        printf("\trep_%s_qvalue",ARGV[i])
        delete ARGV[i];
    }
    printf("\n")
}
{
    print $1,$2,$3,$23,$12,$18
}
END{
}


