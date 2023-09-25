#!/bin/bash

tif_directory="./"

if [ $# -gt 0 ]; then
    tif_directory="$1"
fi

for file in "$tif_directory"/*.TIF; do
    if [ -f "$file" ] &&  [[ "$file" != *FIT.TIF ]] ; then
    python3 GausBeamFit.py "$file"
    fi
done