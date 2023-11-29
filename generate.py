#!/usr/bin/env python3

from datetime import datetime, UTC
from jinja2 import Environment, FileSystemLoader

import tables
import sys


def handle_socs():

    socs = {}

    for soc in tables.socs:
        soc["core_names"] = []

        aarch32 = False

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

            # try to check core part-revision-variant
            # (like X-Gene 1/2/3)
            core_prv = f'{hex(core["part"])}-{core["revision"]}-' \
                f'{core["variant"]}'
            try:
                soc["core_names"].append(
                    tables.cpu_cores[core["implementer"]]["cores"][
                        core_prv]["name"]
                )
                aarch32 = tables.cpu_cores[
                    core["implementer"]]["cores"][core_prv]["aarch32"]
            except KeyError:
                try:
                    soc["core_names"].append(
                        tables.cpu_cores[core["implementer"]]["cores"][
                            hex(core["part"])]["name"]
                    )
                    aarch32 = tables.cpu_cores[
                        core["implementer"]]["cores"][
                            hex(core["part"])]["aarch32"]
                except KeyError:
                    print(
                        f"Missing name for {hex(core['part'])} for "
                        f"{hex(core['implementer'])}!",
                        file=sys.stderr
                    )
                    sys.exit(-1)

            if aarch32 == "to be set":
                aarch32 = ""
            elif aarch32 is False:
                aarch32 = "NO"

            core["aarch32"] = aarch32

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


def handle_cpu_cores():

    cpu_cores = {}

    for implementer in tables.cpu_cores:

        cpu_cores[implementer] = {}
        for core in tables.cpu_cores[implementer]['cores']:
            try:
                cpu_cores[implementer][int(core, base=16)] = tables.cpu_cores[
                    implementer]['cores'][core]
            except ValueError:
                pass

    return cpu_cores


def generate_html_file(socs, cpu_features, cpu_cores):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader,
                      trim_blocks=True,
                      lstrip_blocks=True)

    template = env.get_template("arm-socs.html.j2")

    output = template.render(
        generate_time=datetime.strftime(datetime.now(UTC), "%d %B %Y %H:%M"),
        socs=socs,
        cpu_features=cpu_features,
        cpu_cores=cpu_cores,
    )
    print(output)


if __name__ == "__main__":
    socs = handle_socs()
    cpu_cores = handle_cpu_cores()
    cpu_features = handle_cpu_features()
    generate_html_file(socs, cpu_features, cpu_cores)
