PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_top"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_parts"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_races"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_plc"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_items"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_rest"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_a"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_b"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_c"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_d"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_music"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_override"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_override2"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_creature"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_creature2"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_skybox"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose amia_weapons"

PowerShell -NoProfile -ExecutionPolicy Bypass -Command "docker run --rm -t -u ${id -u}:${id -g} -v ${pwd}:/nasher cltalmadge/nasher:0.20.2 pack --verbose tlk"
