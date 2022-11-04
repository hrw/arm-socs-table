# SPDX-License-Identifier: GPL-2.0-or-later

# Some code taken from util-linux/sys-utils/lscpu-arm.c
#

import yaml

# taken from util-linux/sys-utils/lscpu-arm.c
cpu_cores = {
    0x0: {
        "name": "QEMU",
        "0x51": "Max",
    },
    0x41: {
        "name": "ARM",
        "0x0": "?",
        "0xd03": "Cortex-A53",
        "0xd04": "Cortex-A35",
        "0xd05": "Cortex-A55",
        "0xd06": "Cortex-A65",
        "0xd07": "Cortex-A57",
        "0xd08": "Cortex-A72",
        "0xd09": "Cortex-A73",
        "0xd0a": "Cortex-A75",
        "0xd0b": "Cortex-A76",
        "0xd0c": "Neoverse-N1",
        "0xd0d": "Cortex-A77",
        "0xd0e": "Cortex-A76AE",
        "0xd13": "Cortex-R52",
        "0xd20": "Cortex-M23",
        "0xd21": "Cortex-M33",
        "0xd40": "Neoverse-V1",
        "0xd41": "Cortex-A78",
        "0xd42": "Cortex-A78AE",
        "0xd43": "Cortex-A65AE",
        "0xd44": "Cortex-X1",
        "0xd46": "Cortex-A510",
        "0xd47": "Cortex-A710",
        "0xd48": "Cortex-X2",
        "0xd49": "Neoverse-N2",
        "0xd4a": "Neoverse-E1",
        "0xd4b": "Cortex-A78C",
        "0xd4c": "Cortex-X1C",
        "0xd4d": "Cortex-A715",
        "0xd4e": "Cortex-X3",
    },
    0x42: {
        "name": "Broadcom",
        "0x0f": "Brahma-B15",
        "0x100": "Brahma-B53",
        "0x516": "ThunderX2",
    },
    0x43: {
        "name": "Cavium",
        "0x0a0": "ThunderX",
        "0x0a1": "ThunderX-88XX",
        "0x0a2": "ThunderX-81XX",
        "0x0a3": "ThunderX-83XX",
        "0x0af": "ThunderX2-99xx",
    },
    0x46: {
        "name": "Fujitsu",
        "0x1": "A64FX",
    },
    0x48: {
        "name": "HiSilicon",
        "0xd01": "Kunpeng-920",
    },
    0x4E: {
        "name": "NVIDIA",
        "0x000": "Denver",
        "0x003": "Denver 2",
        "0x004": "Carmel",
    },
    0x50: {
        "name": "APM",
        "0x0": "X-Gene",
    },
    0x51: {
        "name": "Qualcomm",
        "0x00f": "Scorpion",
        "0x02d": "Scorpion",
        "0x04d": "Krait",
        "0x06f": "Krait",
        "0x201": "Kryo",
        "0x205": "Kryo",
        "0x211": "Kryo",
        "0x800": "Falkor-V1/Kryo",
        "0x801": "Kryo-V2",
        "0x802": "Kryo-3XX-Gold",
        "0x803": "Kryo-3XX-Silver",
        "0x804": "Kryo-4XX-Gold",
        "0x805": "Kryo-4XX-Silver",
        "0xc00": "Falkor",
        "0xc01": "Saphira",
    },
    0x53: {
        "name": "Samsung",
        "0x01": "exynos-m1",
    },
    0x56: {
        "name": "Marvell",
        "0x131": "Feroceon-88FR131",
        "0x581": "PJ4/PJ4b",
        "0x584": "PJ4B-MP",
    },
    0x61: {
        "name": "Apple",
        "0x20": "Icestorm-A14",
        "0x21": "Firestorm-A14",
        "0x22": "Icestorm-M1",
        "0x23": "Firestorm-M1",
        "0x24": "Icestorm-M1-Pro",
        "0x25": "Firestorm-M1-Pro",
        "0x28": "Icestorm-M1-Max",
        "0x29": "Firestorm-M1-Max",
        "0x30": "Blizzard-A15",
        "0x31": "Avalanche-A15",
        "0x32": "Blizzard-M2",
        "0x33": "Avalanche-M2",
    },
    0x70: {
        "name": "Phytium",
        "0x660": "FTC660",
        "0x661": "FTC661",
        "0x662": "FTC662",
        "0x663": "FTC663",
    },
}

cpu_features = {
    "fp": {
        "archv": 8.0,
    },
    "asimd": {
        "archv": 8.0,
    },
    "evtstrm": {
        "archv": 8.0,
    },
    "aes": {
        "archv": 8.0,
    },
    "pmull": {
        "archv": 8.0,
    },
    "sha1": {
        "archv": 8.0,
    },
    "sha2": {
        "archv": 8.0,
    },
    "crc32": {
        "archv": 8.0,
    },
    "atomics": {
        "archv": 8.0,
    },
    "fphp": {
        "archv": 8.0,
    },
    "asimdhp": {
        "archv": 8.0,
    },
    "cpuid": {
        "archv": 8.0,
    },
    "asimdrdm": {
        "archv": 8.0,
    },
    "jscvt": {
        "archv": 8.0,
    },
    "fcma": {
        "archv": 8.0,
    },
    "lrcpc": {
        "archv": 8.0,
    },
    "dcpop": {
        "archv": 8.0,
    },
    "sha3": {
        "archv": 8.0,
    },
    "asimddp": {
        "archv": 8.0,
    },
    "sha512": {
        "archv": 8.0,
    },
    "asimdfhm": {
        "archv": 8.0,
    },
    "dit": {
        "archv": 8.0,
    },
    "uscat": {
        "archv": 8.0,
    },
    "ilrcpc": {
        "archv": 8.0,
    },
    "flagm": {
        "archv": 8.0,
    },
    "sb": {
        "archv": 8.0,
    },
    "paca": {
        "archv": 8.0,
    },
    "pacg": {
        "archv": 8.0,
    },
    "dcpodp": {
        "archv": 8.0,
    },
    "flagm2": {
        "archv": 8.0,
    },
    "frint": {
        "archv": 8.0,
    },
    "ssbs": {
        "archv": 8.0,
    },
    "sve": {
        "archv": 8.0,
    },
    "sm3": {
        "archv": 8.0,
    },
    "sm4": {
        "archv": 8.0,
    },
    "svei8mm": {
        "archv": 8.0,
    },
    "svebf16": {
        "archv": 8.0,
    },
    "i8mm": {
        "archv": 8.0,
    },
    "bf16": {
        "archv": 8.0,
    },
    "dgh": {
        "archv": 8.0,
    },
    "rng": {
        "archv": 8.0,
    },
}

with open("socs.yml") as yml:
    socs = yaml.safe_load(yml)
