#!/usr/bin/env python3

import os
import sys
import tables
import yaml

def hexint_presenter(dumper, data):
    return dumper.represent_int(hex(data))


yaml.add_representer(int, hexint_presenter)

for soc in tables.socs:
    cores = []
    for part in soc['part']:
        try:
            if soc['revision']:
                pass
        except KeyError:
            soc['revision'] = 0
        try:
            if soc['variant']:
                pass
        except KeyError:
            soc['variant'] = 0
        cores.append({
            'part': part,
            'implementer': soc['implementer'],
            'revision': soc['revision'],
            'variant': soc['variant'],
        })
    soc['cores'] = cores
    del soc['implementer']
    del soc['part']
    del soc['variant']
    del soc['revision']

with open("data/socs.yml", "w") as yml:
    yaml.dump(tables.socs, yml)
