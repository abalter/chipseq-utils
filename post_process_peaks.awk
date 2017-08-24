#!/bin/awk -f
BEGIN{
    OFS="\t";
    printf("#chr\tstart\tstop\tlog2_fold\tChIP\tinput\tq_value");
    printf("\n")
}
/^#/{next}
{
    print $1,$2,$3,log(($10+1)/($11+1))/log(2),$4,$5,$9;
}
END{
}


