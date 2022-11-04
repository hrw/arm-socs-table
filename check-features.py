#!/usr/bin/env python3

import tables

for soc in tables.socs:
    for feature in soc["features"]:
        if feature not in tables.cpu_features:
            print(
                f"""
"{feature}": {{
    "archv": 8.0,
}}, """
            )
