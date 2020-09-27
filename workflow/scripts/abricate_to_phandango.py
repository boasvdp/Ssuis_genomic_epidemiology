#!/usr/bin/env python3

import pandas as pd
import argparse
import sys

parser = argparse.ArgumentParser(description='Convert an ABRicate summary to Phandango format')

parser.add_argument('input', help="Input ABRicate summary file", type=str)
parser.add_argument("-o", "--output", dest="output", help="Output Phandango file", type=str, default=sys.stdout)

args = parser.parse_args()

df = pd.read_csv(args.input, sep = '\t', index_col=0)
df.replace('.', 'absent', inplace=True)
df.replace('[0-9.][0-9.]*', 'present', regex=True, inplace=True)
df['name'] = df.index
df['name'].replace('_[A-Za-z]{3,6}.tsv', '', regex=True, inplace=True)
df['name'].replace('abricate_out/[A-Za-z]{3,6}/', '', regex=True, inplace=True)
df.set_index('name', inplace=True)
df.drop('NUM_FOUND', axis=1, inplace=True)
df.to_csv(args.output, sep = ',')
