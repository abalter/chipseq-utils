#!/bin/awk

BEGIN { 
    col = ARGV[1];
    #print "col=" col;
    ARGV[1] = "";
    min = 1e999;
    max = -1e999; 
}

{
    min = $col<min ? $col : min;
    max = $col>max ? $col : max;
}

END { 
    print min, max;
}

