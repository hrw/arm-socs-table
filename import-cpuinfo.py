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
    "announce": {"time": ""},
    "cores": [],
    "features": [],
    "name": sys.argv[2],
    "vendor": sys.argv[3]
}

for soc in tables.socs:
    if new_soc["name"] == soc["name"]:
        if len(sys.argv) > 4 and sys.argv[4] == '--force':
            tables.socs.remove(soc)
        else:
            print(f"{new_soc['name']} is already present")
            sys.exit(-1)

cores = {}

for line in cpu_data:
    if line.startswith("Features") and not new_soc["features"]:
        new_soc["features"] = line.partition(":")[2].strip().split(" ")

        for feature in new_soc["features"]:
            if feature not in tables.cpu_features:
                print(f"'{feature}' is not present in "
                      f"data/cpu_features.yml file")
                sys.exit(-1)

        # some old Android kernels have both arm32 and aarch64 flags
        for arm32_flag in ["edsp", "fastmult", "fpa", "half", "idiva", "idivt",
                           "iwmmxt", "java", "lpae", "neon", "swp", "thumb",
                           "thumbee", "tls", "vfp", "vfpd32", "vfpv3",
                           "vfpv3d16", "vfpv4"]:
            try:
                new_soc["features"].remove(arm32_flag)
            except ValueError:
                # flag is not present
                pass

    elif line.startswith("CPU implementer"):
        implementer = int(line.partition(":")[2].strip(), base=16)
        try:
            if tables.cpu_cores[implementer]:
                pass
        except KeyError:
            print(f"Implementer {implementer} is missing.")
            sys.exit(-1)
    elif line.startswith("CPU variant"):
        variant = int(line.partition(":")[2].strip(), base=16)
    elif line.startswith("CPU part"):
        line_part = int(line.partition(":")[2].strip(), base=16)
        try:
            if tables.cpu_cores[implementer]["cores"][hex(line_part)]:
                pass
        except KeyError:
            print(f"Core {hex(line_part)} for "
                  f"{tables.cpu_cores[implementer]['name']} is missing.")
            sys.exit(-1)
    elif line.startswith("CPU revision"):
        revision = int(line.partition(":")[2].strip(), base=16)
        # "CPU revision" line is last in block so we have all core data
        try:
            if cores[line_part]:
                pass
        except KeyError:
            cores[line_part] = {
                'part': line_part,
                'implementer': implementer,
                'variant': variant,
                'revision': revision,
            }

for core in cores:
    new_soc["cores"].append(cores[core])

tables.socs.append(new_soc)


with open("data/socs.yml", "w") as yml:
    yaml.dump(sorted(tables.socs, key=lambda d: d['vendor']), yml)
