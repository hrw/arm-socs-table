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
    if len(cpu_data) < 8:
        print("procinfo dump is too short")
        sys.exit(-1)

new_soc = {
    "announce": {"time": ""},
    "cores": [],
    "features": [],
    "name": sys.argv[2],
    "vendor": sys.argv[3]
}

for soc in tables.rv_socs:
    if new_soc["name"] == soc["name"]:
        if len(sys.argv) > 4 and sys.argv[4] == '--force':
            tables.socs.remove(soc)
        else:
            print(f"{new_soc['name']} is already present")
            sys.exit(-1)

cores = {}

for line in cpu_data:
    if line.startswith("isa") and not new_soc["features"]:
        new_soc["features"] = line.partition(":")[2].strip().split("_")

        for feature in new_soc["features"]:
            if feature.startswith("rv64imafdc"):
                new_soc["features"].append("rv64gc")
                new_soc["features"].remove(feature)
                if feature != "rv64imafdc":
                    feature = feature.replace("rv64imafdc", "")
                    for feat in feature:
                        new_soc["features"].append(feat)
                # we skip check
                continue

            if feature not in tables.rv_cpu_features:
                print(f"'{feature}' is not present in "
                      f"data/rv_cpu_features.yml file")
                sys.exit(-1)

    elif line.startswith("mmu"):
        mmu = line.partition(":")[2].strip()
    elif line.startswith("mvendorid"):
        implementer = int(line.partition(":")[2].strip(), base=16)
        try:
            if tables.rv_cpu_cores[implementer]:
                pass
        except KeyError:
            print(f"Implementer {implementer} is missing.")
            sys.exit(-1)
    elif line.startswith("marchid"):
        marchid = int(line.partition(":")[2].strip(), base=16)
        try:
            if tables.rv_cpu_cores[implementer]["cores"][hex(marchid)]:
                pass
        except KeyError:
            print(f"Core {hex(marchid)} for "
                  f"{tables.rv_cpu_cores[implementer]['name']} is missing.")
            sys.exit(-1)
    elif line.startswith("mimpid"):
        mimpid = int(line.partition(":")[2].strip(), base=16)
        # "mimpid" line is last we parse in block so we have all core data
        try:
            if cores[marchid]:
                pass
        except KeyError:
            cores[marchid] = {
                'implementer': implementer,
                'marchid': marchid,
                'mimpid': mimpid,
                'mmu': mmu,
            }

for core in cores:
    new_soc["cores"].append(cores[core])

tables.rv_socs.append(new_soc)


with open("data/rv_socs.yml", "w") as yml:
    yaml.dump(sorted(tables.rv_socs, key=lambda d: d['vendor']), yml)
