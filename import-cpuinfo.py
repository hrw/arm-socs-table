#!/usr/bin/env python3

import os
import sys
import tables
import yaml

if len(sys.argv) < 4:
    print(f"Usage: {os.path.basename(__file__)} "
          "cpuinfo-file soc-name soc-vendor")
    sys.exit(-1)


def hexint_presenter(dumper, data):
    return dumper.represent_int(hex(data))


yaml.add_representer(int, hexint_presenter)

cpu_data = []

with open(sys.argv[1]) as cpuinfo:
    cpu_data = cpuinfo.readlines()

new_soc = {
    "part": [],
    "features": [],
    "name": sys.argv[2],
    "vendor": sys.argv[3]
}

for line in cpu_data:
    if line.startswith("Features") and not new_soc["features"]:
        new_soc["features"] = line.partition(":")[2].strip().split(" ")
    elif line.startswith("CPU implementer"):
        new_soc["implementer"] = int(line.partition(":")[2].strip(), base=16)
    elif line.startswith("CPU variant"):
        new_soc["variant"] = int(line.partition(":")[2].strip(), base=16)
    elif line.startswith("CPU part"):
        line_part = int(line.partition(":")[2].strip(), base=16)
        if line_part not in new_soc["part"]:
            new_soc["part"].append(line_part)
    elif line.startswith("CPU revision"):
        new_soc["revision"] = int(line.partition(":")[2].strip(), base=16)

tables.socs.append(new_soc)

with open("socs.yml", "w") as yml:
    yaml.dump(tables.socs, yml)
