#!/bin/bash

CURDIR=$( cd $( dirname "$0" ) && pwd )
BENCHDIR=$( dirname "$CURDIR" )
TOPDIR=$( dirname "$BENCHDIR" )
MEMUSG="${TOPDIR}"/scripts/memusg

if [ ! -d "${TOPDIR}"/scripts ]; then
    echo "top-level directory could not be found; exiting"
    exit -1
fi

BIG="${TOPDIR}"/data/big.json

if [ ! -s "$BIG" ]; then
    echo "Creating test data"
    "${TOPDIR}"/scripts/generate-big-json.sh > "$BIG"
fi

for d in "$CURDIR"/*; do
    if [ -d "$d" -a -s "$d"/setup.sh -a -s "$d"/run.sh ]; then
	# clear cache for timing setup
	if [ -d "$d"/__pycache__ ]; then
	    rm -rf "$d"/__pycache__
	fi

	name=$( basename "$d" )
	echo
	echo "#### $name ################"
	echo
	pushd "$d"
        echo "setup"
	./setup.sh
	sleep .2
        echo
        echo "run on big file"
	./run.sh "$BIG"
	sleep .2
	popd
    fi
done
