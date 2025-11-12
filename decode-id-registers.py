#!/bin/python3

import tables
import yaml


def hexint_presenter(dumper, data):
    return dumper.represent_int(hex(data))


yaml.add_representer(int, hexint_presenter)

features = {}
for feature in tables.arch_features['features'].keys():
    features[feature] = False


def handle_register(register_name, register_value):
    register_data = tables.arch_features['id_registers'][register_name]

    for offset in register_data.keys():
        value = (register_value >> (offset - 3)) & 0x0f
        try:
            for feature in register_data[offset][value]:
                features[feature] = True
        except KeyError:
            pass


for core in tables.cpu_cores[65]['cores']:

    for feature in tables.arch_features['features'].keys():
        features[feature] = False

    core_data = tables.cpu_cores[65]['cores'][core]
    if 'registers' in core_data:
        print(f"CPU core {core_data['name']} has registers")

        for register in core_data['registers']:
            print(f'{register} = {core_data['registers'][register]}')
            handle_register(register,
                            int(core_data['registers'][register], 16))

        core_data['features'] = []
        for feature in features:
            if features[feature]:
                core_data['features'].append(feature)

        tables.cpu_cores[65]['cores'][core] = core_data

with open("data/cpu_cores.yml", "w") as yml:
    yaml.dump(tables.cpu_cores, yml)
