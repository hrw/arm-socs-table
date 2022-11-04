#!/usr/bin/env python3

import tables
import yaml

for soc in tables.socs:
    for feature in soc["features"]:
        if feature not in tables.cpu_features:
            tables.cpu_features[feature] = {"archv": 8.0}

with open("cpu_features.yml", "w") as yml:
    yaml.dump(tables.cpu_features, yml)
