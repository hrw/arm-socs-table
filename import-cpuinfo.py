#!/usr/bin/env python3

import tables
import sys

cpu_data = []

with open(sys.argv[1]) as cpuinfo:
    cpu_data = cpuinfo.readlines()

features = ""
implementer = 0
variant = 0
part = []
revision = 0

for line in cpu_data:
    if line.startswith("Features") and features == "":
        features = line.partition(":")[2].strip().split(" ")
    elif line.startswith("CPU implementer") and not implementer:
        implementer = line.partition(":")[2].strip()
    elif line.startswith("CPU variant"):
        variant = line.partition(":")[2].strip()
    elif line.startswith("CPU part"):
        line_part = line.partition(":")[2].strip()
        if line_part not in part:
            part.append(line_part)
    elif line.startswith("CPU revision"):
        revision = line.partition(":")[2].strip()

print("{")
print(f"    'name': '{sys.argv[2]}',")
print(f"    'features': {features},")
print(f"    'implementer': {implementer},")
print(f"    'part': {sorted(part, reverse=True)},")
print(f"    'revision': {revision},")
print(f"    'variant': {variant}")
print("},")
