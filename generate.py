#!/usr/bin/env python3

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import tables
import sys


def handle_socs():

    socs = tables.socs.copy()

    for soc in socs:
        try:
            soc["implementer_name"] = tables.cpu_cores[soc["implementer"]][
                "name"
            ]
        except KeyError:
            print(
                f"Missing name for {hex(soc['implementer'])} core"
                " implementer!"
            )
            sys.exit(-1)

        soc["core_names"] = []
        for core in sorted(soc["part"], reverse=True):
            try:
                soc["core_names"].append(
                    tables.cpu_cores[soc["implementer"]][hex(core)]
                )
            except KeyError:
                print(
                    f"Missing name for {hex(core)} for "
                    f"{hex(soc['implementer'])}!"
                )
                sys.exit(-1)

    return socs


def generate_html_file(socs):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)

    template = env.get_template("arm-socs.html.j2")

    output = template.render(
        generate_time=datetime.strftime(datetime.utcnow(), "%d %B %Y %H:%M"),
        socs=socs,
        cpu_features=tables.cpu_features,
        minify=True,
    )
    print(output)


if __name__ == "__main__":
    socs = handle_socs()
    generate_html_file(socs)
