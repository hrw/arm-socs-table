# SPDX-License-Identifier: GPL-2.0-or-later

# Some code taken from util-linux/sys-utils/lscpu-arm.c
#

import yaml

# taken from util-linux/sys-utils/lscpu-arm.c

with open("data/cpu_cores.yml") as yml:
    cpu_cores = yaml.safe_load(yml)

with open("data/socs.yml") as yml:
    socs = yaml.safe_load(yml)

with open("data/cpu_features.yml") as yml:
    cpu_features = yaml.safe_load(yml)

with open("data/arch_features.yml") as yml:
    arch_features = yaml.safe_load(yml)
