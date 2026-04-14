#!/usr/bin/env python3

from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
from operator import attrgetter

import tables
import sys


def handle_socs():

    socs = {}

    for soc in tables.rv_socs:
        soc["core_names"] = []
        if "announce" not in soc or soc["announce"]["time"] is None:
            soc["announce"] = {"time": " "}

        for core in soc["cores"]:
            try:
                core["implementer_name"] = tables.rv_cpu_cores[
                    core["implementer"]]["name"]
            except KeyError:
                print(
                    f"Missing name for {hex(core['implementer'])} core"
                    " implementer!",
                    file=sys.stderr
                )
                sys.exit(-1)

            soc["core_names"].append(
                tables.rv_cpu_cores[core["implementer"]]["cores"][
                    hex(core["marchid"])]["name"]
            )

        socs[f"{soc['vendor']}-{soc['name']}"] = soc

    sorted_socs = []

    for key in sorted(socs.keys()):
        sorted_socs.append(socs[key])

    return sorted_socs


def handle_cpu_features():

    cpu_features = {}

    for feature in tables.rv_cpu_features:
        if 'rva' not in tables.rv_cpu_features[feature]:
            print(f"Missing RVA for {feature}")
            sys.exit(-1)

        rva = tables.rv_cpu_features[feature]["rva"]
        if rva is None:
            rva = " "
            tables.rv_cpu_features[feature]["rva"] = " "
        if not rva in cpu_features:
            cpu_features[rva] = {}

        cpu_features[rva][feature] = tables.rv_cpu_features[feature]

    return cpu_features


def handle_cpu_cores():

    cpu_cores = {}

    for implementer in tables.rv_cpu_cores:

        cpu_cores[implementer] = {}
        for core in tables.rv_cpu_cores[implementer]['cores']:
            try:
                cpu_cores[implementer][int(core, base=16)] = tables.rv_cpu_cores[
                    implementer]['cores'][core]
            except ValueError:
                pass

    return cpu_cores


def generate_html_file(socs, cpu_features, cpu_cores):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader,
                      trim_blocks=True,
                      lstrip_blocks=True)

    template = env.get_template("rv-socs.html.j2")

    output = template.render(
        generate_time=datetime.strftime(datetime.now(timezone.utc),
                                        "%d %B %Y %H:%M"),
        socs=socs,
        cpu_features=cpu_features,
        cpu_cores=cpu_cores,
        git_repo="arm-socs-table",
    )
    print(output)


if __name__ == "__main__":
    socs = handle_socs()
    cpu_cores = handle_cpu_cores()
    cpu_features = handle_cpu_features()
    generate_html_file(socs, cpu_features, cpu_cores)
