#!/bin/bash

set -euo pipefail

if [[ ! -f $1 ]] || [[ -z $2 ]]
then
	echo "Usage: bash $0 [ABRICATE OUTPUT TO FILTER] [MINID THRESHOLD] > [OUTPUT]"
fi

body() {
    IFS= read -r header
    printf '%s\n' "$header"
    "$@"
}

cat $1 | body awk -F "\t" -v MINID=$2 '$11 >= MINID {print $0}'
