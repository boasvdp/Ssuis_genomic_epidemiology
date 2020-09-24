#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Summarise S. suis isolates')

parser.add_argument('list', help="List of isolates to summarise", type=str)
parser.add_argument('--mlst', dest="mlst", help="mlst output directory", type=str, default='mlst')
parser.add_argument('--amrfinder', dest="amrfinder", help="AMRFinder output directory", type=str, default='amrfinder_out')
parser.add_argument('--serotype', dest="serotype", help="Results file from Ssuis_serotyping pipeline", type=str, default='Results_FinalResults.txt')
parser.add_argument('--quast', dest="quast", help="Quast directory", type=str, default='quast_out')
parser.add_argument('--metadata', dest="metadata", help="Metadata file", type=str, default='config/cleaned_metadata_42.csv')
parser.add_argument('--coverage', dest="coverage", help="Coverage directory", type=str, default='coverage_out')
parser.add_argument('--kraken', dest="kraken", help="Kraken2 output directory", type=str, default='kraken_out')

args = parser.parse_args()

isolates = open(args.list, "r+")
isolate_list = list(isolates.readlines())
isolates.close()

print('isolate', 'country', 'year', 'source', 'host_birthyear', 'host_sex', 'host_health', 'occupational_risk', 'species', 'pct_species', 'reads_species', 'serotype', 'ST', 'epf', 'mrp', 'sly', 'erm_genes', 'tet_genes', 'ant_genes', 'dfr_genes', 'number_contigs', 'N50', 'largest_contig', 'total_size', 'coverage', sep = ',')

for isolate in isolate_list:
  # Remove trailing newline
  isolate = isolate.rstrip('\n')

  # Get metadata
  m = open(args.metadata)
  lines = m.readlines()
  m.close()

  for line in lines:
    if isolate == line.split(',')[0]:
      COUNTRY = line.split(',')[1]
      YEAR = line.split(',')[3]
      SOURCE = line.split(',')[4]
      HOST_BIRTHYEAR = line.split(',')[5]
      HOST_SEX = line.split(',')[6]
      HOST_HEALTH = line.split(',')[7]
      OCC_RISK = line.split(',')[8].rstrip('\n')

  # Get Kraken2
  k = open(args.kraken + '/' + isolate + '_kraken2_report.txt', 'r')
  lines = k.readlines()
  k.close()

  for line in lines:
    if line.split('\t')[3] == 'S':
      SPECIES = line.split('\t')[5].lstrip(' ').rstrip('\n')
      PCT = line.split('\t')[0].lstrip(' ')
      READS = line.split('\t')[2]
      break

  # Get ST
  t = open(args.mlst + '/' + isolate + ".tsv")
  ST = str(t.readline().split('\t')[2])
  t.close()

  # Serotype
  s = open(args.serotype)
  lines = list(s.readlines())
  s.close()

  for line in lines:
    if isolate == line.split('\t')[0]:
      SEROTYPE = line.split('\t')[1]
      EPF = line.split('\t')[11]
      MRP = line.split('\t')[12]
      SLY = line.split('\t')[13].rstrip('\n')

  # Get AMR genes and put lines in a list to reuse
  a = open(args.amrfinder + '/' + isolate + ".tsv")
  lines = list(a.readlines())
  a.close()

  # erm(B) genes
  ERM = ''
  for line in lines:
    if 'erm(B)' in line.split('\t')[5]:
      ERM = ERM + line.split('\t')[5] + '|'
  ERM = ERM.rstrip('|')
  if ERM == '':
    ERM = 'None'

  # tet genes
  TET = ''
  for line in lines:
    if 'tet' in line.split('\t')[5]:
      TET = TET + line.split('\t')[5] + '|'
  TET = TET.rstrip('|')
  if TET == '':
    TET = 'None'

  # ant genes
  ANT = ''
  for line in lines:
    if 'ant' in line.split('\t')[5]:
      ANT = ANT + line.split('\t')[5] + '|'
  ANT = ANT.rstrip('|')
  if ANT == '':
    ANT = 'None'

  # dfr genes
  DFR = ''
  for line in lines:
    if 'dfr' in line.split('\t')[5]:
      DFR = DFR + line.split('\t')[5] + '|'
  DFR = DFR.rstrip('|')
  if DFR == '':
    DFR = 'None'

  # Get quast
  q = open(args.quast + '/' + isolate + "/report.tsv")
  lines = q.readlines()
  q.close()

  for line in lines:
    if line.split('\t')[0] == '# contigs':
      CONTIGS = line.split('\t')[1].rstrip('\n')
    if line.split('\t')[0] == 'Largest contig':
      LARGEST = line.split('\t')[1].rstrip('\n')
    if line.split('\t')[0] == 'Total length':
      SIZE = line.split('\t')[1].rstrip('\n')
    if line.split('\t')[0] == 'N50':
      N50 = line.split('\t')[1].rstrip('\n')

  # Get coverage
  c = open(args.coverage + '/' + isolate + '.txt')
  COVERAGE = str(c.readline().rstrip('\n'))
  c.close()

  print(isolate, COUNTRY, YEAR, SOURCE, HOST_BIRTHYEAR, HOST_SEX, HOST_HEALTH, OCC_RISK, SPECIES, PCT, READS, SEROTYPE, ST, EPF, MRP, SLY, ERM, TET, ANT, DFR, CONTIGS, N50, LARGEST, SIZE, COVERAGE, sep = ',')
