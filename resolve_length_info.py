#!/usr/bin/env python
#coding: utf-8

from pbcore.io import FastaReader
from multiprocessing import Pool
from collections import defaultdict
import sys
import re
import math


def resolve_length_info(seq):

    well, data_list = seq
    data_list.sort()
    first_start = data_list[0][0]

    if first_start < 100:
        num_threshold = 3
    else:
        num_threshold = 4
    if len(data_list) < num_threshold:
        return None

    #print "num_threshold =", num_threshold

    length_dict = {}
    average_length = 0
    for index in range(len(data_list) - 1):
        if num_threshold == 4 and index == 0:
            continue
        start, end = data_list[index]
        length_dict[index] = end - start
        average_length += end - start
    if average_length / len(length_dict) < 2200:
        return None

    #print length_dict

    separate_index = set()
    for index, length in length_dict.items():
        for index_, length_ in length_dict.items():
            if index_ != index and length_ >= length * 1.5:
                separate_index.add(index_)
    if len(separate_index) == 0:
        return None

    #print separate_index

    normal_index = set()
    normal_length = 0
    for index, length in length_dict.items():
        if index not in separate_index:
            normal_index.add(index)
            normal_length += length
    normal_length /= len(normal_index)

    separate_dict = {}
    for index in separate_index:
        separate_num = float(length_dict[index]) / normal_length
        decimal, integer = math.modf(separate_num)
        if decimal <= 0.5:
            separate_num = integer
        else:
            separate_num = integer + 1
        if separate_num > 1:
            separate_dict[index] = separate_num
    if len(separate_dict) == 0:
        #print "***size of separate_dict is 0!***"
        return None

    return well, data_list, separate_dict


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="determine the number of splitting adaptor unremoved subreads")
    parser.add_argument('fasta_file', help="a file that contains the subread information")
    parser.add_argument('--n_core', type=int, default=12, help="number of processes")
    #parser.add_argument('--len_th', type=int, default=1, help="length threshold of k-mer matching region")
    args = parser.parse_args()
    exe_pool = Pool(args.n_core)

    fasta_file = args.fasta_file
    #length_threshold = args.len_th

    fasta = FastaReader(fasta_file)
    header_pattern = r'(.*)\/(.*)_(.*)'
    re_pattern = re.compile(header_pattern)

    seqs = defaultdict(list)
    for subread in fasta:
        matched = re_pattern.search(subread.name).groups()
        well, start, end = matched
        start = int(start)
        end = int(end)
        seqs[well].append( (start, end) )

    #for well, tup in seqs.items():
    #    print well, tup
    
    """
    for obj in seqs.items():   # single-process
        res = resolve_length_info(obj)
        if res is not None:
            print res
    """

    for res in exe_pool.imap(resolve_length_info, seqs.items()):
        if res is not None:
            well, data_list, separate_dict = res
            for index, sep_num in separate_dict.items():
                print well, data_list[index][0], data_list[index][1], sep_num
