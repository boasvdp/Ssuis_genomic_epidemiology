#!/usr/bin/env python3

# Import modules
import sys
import colorbrewer as cb
import pandas as pd
import argparse
import os
import numpy as np
import random

# import local module from itolparser.py
import itolparser

# Parse arguments
parser = argparse.ArgumentParser(description='Find within and between cluster comparisons based on SNP distances and fastBAPS clustering.')

parser.add_argument('input', help="Input table with categorical metadata in .tsv format unless otherwise specified", type=str)
parser.add_argument("-o", "--outdir", dest="outdir", default="./", metavar="OUTDIR", help="Output directory to write files to", type=str)
parser.add_argument("-d", "--delimiter", dest="delim", default="\t", metavar="DELIMITER", help="Field delimiter of input table (e.g. '\t', ',', ';')", type=str)
parser.add_argument("--margin", dest="margin", default="5", metavar="STRIP MARGIN", help="Size of margin specified in iTOL file", type=str)
parser.add_argument("--stripwidth", dest="stripwidth", default="50", metavar="STRIP WIDTH", help="Strip width specified in iTOL file", type=str)
parser.add_argument("--maxcategories", dest="maxcategories", default = 18, metavar="MAX \# CATEGORIES", help="Maximum number of categories to not get assigned to other", type=int)
parser.add_argument("--ignore", dest="ignore", metavar="IGNORELIST", help="Columns to ignore", type=str)

args = parser.parse_args()

# Read in typing/metadata table using the provided delimiter
df = pd.read_csv(args.input, sep = args.delim)

# Make a list of hexadecimal values to generate random hex colours from later, convert to strings
list_random = list(range(10)) + ['a' ,'b' ,'c' ,'d' ,'e', 'f']
list_random = [format(x) for x in list_random]

# Get column name of samples
id_name = df.columns[0]

# Make output directory if it does not exist yet
if not os.path.exists(args.outdir):
  os.makedirs(args.outdir)

# Loop over columns
for i in range(1, len(df.columns)):
  # Subset column (with sample names) and get name
  tmpdf = df.iloc[:,[0,i]]
  name = tmpdf.columns[1]

  IGNORE = 0
  if args.ignore is not None:
    for ignorename in args.ignore.split(','):
      if name == ignorename:
        IGNORE += 1
        print(name + " is in " + str(args.ignore) + " and will thus be ignored.")
        print(name, IGNORE)
  if IGNORE > 0:
    continue

  # Get unique values and remove specified items
  list_vals = sorted(tmpdf.dropna()[name].unique())
  list_removevals = ['None', 'none', 'Absent', 'absent', '0', 0, 'nan', 'NaN', 'NA', '-']
  for removeval in list_removevals:
    if removeval in list_vals:
      list_vals.remove(removeval)

  # Check how many unique values exist and define colour scheme based on number
  nr_values = len(list_vals)

  # Get dict
  a_dict = itolparser.create_dicts(tmpdf, name, list_vals)

  # Print full iTOL output
  itolparser.printitol(name, name, id_name, a_dict, a_dict, args.outdir, args.margin, args.stripwidth, tmpdf)

  # If more than 18 values (defined! see big if loop), print filtered up to j max categories
  if nr_values > 18:
    a_dict_alt = itolparser.create_dicts(tmpdf, name, list_vals)
    name_filtered = name + '_filtered'

    # Create smaller dictionary with only key:values to keep from list_include. Manually add the key 'other'
    sub_dict = {l: a_dict_alt[l] for l in list_include}
    sub_dict['other'] = '#bebebe'

    # Print filtered iTOL output
    itolparser.printitol(name, name_filtered, id_name, a_dict_alt, sub_dict, args.outdir, args.margin, args.stripwidth, tmpdf)
