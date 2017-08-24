#!/bin/awk -f

BEGIN{
    OFS="\t";
    printf("#chr\tstart\tstop\tlog2_fold\t-log10q");
    printf("\n")
}
/^#/{next}
{
    print $1,$2,$3,log($11/$12)/log(2),$9;
}
END{
}


