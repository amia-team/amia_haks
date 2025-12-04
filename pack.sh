#!/bin/bash
docker run --rm -t -u $(id -u):$(id -g) -v "$(pwd):/nasher" -v "$(pwd):/root/.local/share/Neverwinter Nights/$1/" cltalmadge/nasher:1.1.1 pack --clean --verbose --packUnchanged --yes $2
