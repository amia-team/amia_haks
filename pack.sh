#!/bin/bash
docker run --rm -t -u $(id -u):$(id -g) -v "$(pwd):/nasher" -v "$(pwd):/root/.local/share/Neverwinter Nights/$1/" nasher pack --clean --verbose --yes $2