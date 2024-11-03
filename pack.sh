#!/bin/bash
docker run --rm -t -u $(id -u):$(id -g) -v "$(pwd):/nasher" -v "$(pwd):/root/.local/share/Neverwinter Nights/$1/" cltalmadge/nasher:0.20.2 pack --clean --verbose --yes $2