#!/usr/bin/env python3

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import tables
import sys


def handle_socs():

    socs = {}

    for soc in tables.socs:
        soc["core_names"] = []
        for core in soc["cores"]:
            try:
                core["implementer_name"] = tables.cpu_cores[
                    core["implementer"]]["name"]
            except KeyError:
                print(
                    f"Missing name for {hex(core['implementer'])} core"
                    " implementer!",
                    file=sys.stderr
                )
                sys.exit(-1)

            try:
                soc["core_names"].append(
                    tables.cpu_cores[core["implementer"]]["cores"][
                        hex(core["part"])]["name"]
                )
            except KeyError:
                print(
                    f"Missing name for {hex(core['part'])} for "
                    f"{hex(core['implementer'])}!",
                    file=sys.stderr
                )
                sys.exit(-1)
        socs[f"{soc['vendor']}-{soc['name']}"] = soc

    sorted_socs = []

    for key in sorted(socs.keys()):
        sorted_socs.append(socs[key])

    return sorted_socs


def handle_cpu_features():

    sorted_cpu_features = {}

    for feature in tables.cpu_features:
        feature_data = tables.cpu_features[feature]
        if not feature_data['archv'] in sorted_cpu_features:
            sorted_cpu_features[feature_data['archv']] = []
        sorted_cpu_features[feature_data['archv']].append(feature)

    cpu_features = {}
    for archv in sorted(sorted_cpu_features):
        for feature in sorted_cpu_features[archv]:
            cpu_features[feature] = tables.cpu_features[feature]

    return cpu_features


def generate_html_file(socs, cpu_features):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)

    template = env.get_template("arm-socs.html.j2")

    output = template.render(
        generate_time=datetime.strftime(datetime.utcnow(), "%d %B %Y %H:%M"),
        socs=socs,
        cpu_features=cpu_features,
        minify=True,
    )
    print(output)


if __name__ == "__main__":
    socs = handle_socs()
    cpu_features = handle_cpu_features()
    generate_html_file(socs, cpu_features)
