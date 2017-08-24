#!/bin/bash


$intersect_command
| bedtools multicov         \ `# get coverage for intersected file`
    -bams $bamfiles         \
    -bed -                  \ `# capture piped intersect file`
| $calc_fold_command        \ `# calculate fold change`
| tee $coverage_file        \ `# save raw coverage file`
| $post_processor $reps -   \ `# create summary file`
> $coverage_summary_file
