#!/usr/bin/env python3

from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader

import tables


def handle_cpu_cores():

    cpu_cores = {}

    implementer = 0x41  # ARM

    cpu_cores[implementer] = {
        "implementer_name": tables.cpu_cores[implementer]["name"],
        "cores": {}
    }

    for core in sorted(tables.cpu_cores[implementer]['cores']):
        try:
            core_data = tables.cpu_cores[implementer]['cores'][core].copy()

            if "features" in core_data and core_data["features"] is not None:
                core_data["features"] = sorted(core_data["features"])
            else:
                core_data["features"] = ""

            cpu_cores[implementer]["cores"][int(core, base=16)] = core_data
        except ValueError:
            pass

    return cpu_cores


def generate_html_file(cpu_cores, arch_features):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader,
                      trim_blocks=True,
                      lstrip_blocks=True)

    template = env.get_template("arm-cpu-cores.html.j2")

    output = template.render(
        generate_time=datetime.strftime(datetime.now(timezone.utc),
                                        "%d %B %Y %H:%M"),
        cpu_cores=cpu_cores,
        arch_features=arch_features,
        git_repo="arm-socs-table",
    )
    print(output)


if __name__ == "__main__":
    cpu_cores = handle_cpu_cores()
    generate_html_file(cpu_cores, tables.arch_features["features"])
