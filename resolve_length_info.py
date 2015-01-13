#!/usr/bin/env python
#coding: utf-8

from pbcore.io import FastaReader
from multiprocessing import Pool
from collections import defaultdict
import sys
import re


def resolve_length_info(seq):
    well, data_list = seq
    if len(data_list) == 1:
    return seq


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="a multi-processes adaptor unremoved subreads finder using subread length infomation")
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
    
    for res in exe_pool.imap(resolve_length_info, seqs.items()):
        print res
