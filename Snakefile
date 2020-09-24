configfile: "config/config.yaml"

IDS, = glob_wildcards("raw_reads/{id}_1.fastq.gz")

f = open("config/excluded_isolates.txt")
lines = f.readlines()
f.close()

INCLUDE = list(IDS)
for line in lines:
  line = line.rstrip('\n')
  if line in INCLUDE:
    INCLUDE.remove(line)

print("All samples: " + str(IDS))
print("Included samples: " + str(INCLUDE))

rule all:
	input:
		expand("kraken_out/{sample}_kraken2_report.txt", sample=IDS),
		expand("amrfinder_out/{sample}.tsv", sample=IDS),
		expand("prokka_out/{sample}/{sample}.gff", sample=IDS),
		"multiqc_out/multiqc_fastp.html",
		expand("mlst/{sample}.tsv", sample=IDS),
		expand("coverage_out/{sample}.txt", sample=IDS),
		expand("abricate_out/{sample}.tsv", sample=IDS),
		"roary_out",
		"iqtree_out",
		"snp-dists_out/snp-dists.tsv",
		"summary.csv",
		"itol_out"

## Workflow ##
include: "workflow/rules/fastp.snake"
include: "workflow/rules/kraken2.snake"
include: "workflow/rules/amrfinder.snake"
include: "workflow/rules/quast.snake"
include: "workflow/rules/shovill.snake"
include: "workflow/rules/mlst.snake"
include: "workflow/rules/coverage.snake"
include: "workflow/rules/prokka.snake"
include: "workflow/rules/abricate.snake"
include: "workflow/rules/multiqc.snake"
include: "workflow/rules/roary.snake"
include: "workflow/rules/iqtree.snake"
include: "workflow/rules/snpdists.snake"
include: "workflow/rules/summary.snake"
include: "workflow/rules/parse_itol.snake"
