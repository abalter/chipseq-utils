#!/bin/env python

import fileinput
import sys
from math import log, log10, log2
from functools import partial

def main(input_file, num_treatments, average_function):
    print("in main")
    for line in input_file: 
        if line[0] == "#":
            continue
        #print(">>" + line)
        line_data = [parseNum(x) for x in line.rstrip().split("\t")]
        num_cols = len(line_data)
        #print("num_cols: " + str(num_cols))

        data_start = num_cols - num_treatments*2
        data_end = data_start + num_treatments - 1  
        control_start = data_end + num_treatments - 1
        control_end = control_start + num_treatments - 1
        
        data = line_data[data_start:data_end+1]
        control = line_data[control_start:control_end+1]

        print("data")
        print(data)
        print("control")
        print(control)

        ### To prevent problems with having zero counts (which could cause
        ### a division by 0 or log of 0) we add 1 to each count before forming
        ### the ratio.
        print(range(num_treatments))
        fold_changes = [ (data[i] + 1) /( control[i] + 1) for i in range(num_treatments)]
        
        average_data_over_control = average_function(fold_changes, num_treatments)
        average_data_over_control = round(average_data_over_control, 3)
        average_control_over_data = average_function([1/f for f in fold_changes], num_treatments)
        average_control_over_data = round(average_control_over_data, 3)

        #print("line data")
        #print(str(line_data))
        line_data += [average_data_over_control, average_control_over_data]
        #print("1 ")
        #print(str(line_data))
        line_data[0:3] = [str(x) for x in line_data[0:3]]
        #print(line_data)
        line_data[3:] = [formatNum(x) for x in line_data[3:]]
        #print(str(line_data))
        print("\t".join(line_data))

def parseNum(x):
    #print("in parseNum, x=" + str(x))
    try:
        return int(x)
    except ValueError:
        pass
    try:
        return float(x)
    except ValueError:
        pass

    return x

def formatNum(x):
    if isinstance(x, str):
        return x

    if x >= 1e7 or x < 1e-3:
        return "{:.2E}".format(x)

    try:
        return "{:d}".format(x)
    except ValueError:
        pass

    try:
        return "{:0.4f}".format(x)
    except ValueError:
        pass

    try:
        return "{:.2E}".format(x)
    except ValueError:
        pass

    return False


def averageGeom(data, N):
    #print(data)
    #print(N)
    prod = 1
    for n in range(N):
        prod *= data[n]
        #print("n: {} prod: {}".format(n,prod))
    avg = prod**(1/N)
    return avg

def averageLinear(data, N):
    sum = 0
    for n in range(N):
        sum += data[n]
    avg = sum/N
    return avg

def averageLog(data, N, b):
    return log(averageGeom(data, N), b)

if __name__ == "__main__":
    import argparse
    from argparse import RawTextHelpFormatter

    parser = argparse.ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    description="""
Adds a log fold change calculation to a coverage file. Assumes the coverage file has the format
        
	chr	start	stop	<other colums>	dataA	dataB	dataC	<...>	controlA	controlB	controlC	<...>

The data and control columns are the coverages for the bam files named in the columns over the
range spcified in the first three columns. 

Two additional columns are added: data/ctrl and ctrl/data.

The coverages must be in the specified order: the data coverage for each treatment followed by
the control coverage for each associated treatment.

calc_fold.py needs to know the number of treatments, which is passed in as a required argument.

The fold changes (coverage ratios) are averaged over the treatments. The averages can be calculated
using the method specified by the `avg` argument which can take one of three values:

    liner: [ data1/contro1 + data2/control2 + ... dataN/controlN ] * (1/N)
    geom: Geometric mean. [ data1/contro1 * data2/control2 * ... dataN/controlN ] ^ (1/N)
    log10,log2: log10(Geometric Mean), log2(Geometric Mean)

The default average method is 'log10'.
        """,
        )

    requiredNamed = parser.add_argument_group('required named arguments')

    parser.add_argument('-i', '--input-file', 
        type=argparse.FileType('r'), 
        default='-',
        nargs='?', 
        help="Input coverage file. If not specified, takes input from stdin."
        )
    requiredNamed.add_argument('-n', '--num-treatments',
        required=True,
        type=int,
        help="The number of treatments. The last 2*n columns are assumed to have the coverage counts.",
        )
    parser.add_argument('-avg', '--average-method', 
        required=False,
        default='log10',
        choices=['linear','geom','log2','log10'],
        help="Specify how to average the fold changes. Choices are: ['log10'|'log2'|'geom'|'linear']. Default is 'log10'.",
        )
    args=parser.parse_args()

    average_method = args.average_method

    while average_method:

        if average_method == 'log10':
            average_function = partial(averageLog, b=10)
            break
        if average_method == 'log2':
            average_function = partial(averageLog, b=2)
            break
        if average_method == 'linear':
            average_function = averageLinear
            break
        if average_method == 'geom':
            average_function = averageGeom
            break
        
        average_function = partial(averageLog, b=10)
        break

    input_file = args.input_file
   
    main(args.input_file, args.num_treatments, average_function)

