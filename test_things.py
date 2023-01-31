
import tables


def test_no_soc_duplicates():
    socs = []

    for soc in tables.socs:
        soc_name = f"{soc['vendor']}:{soc['name']}"
        if soc_name in socs:
            raise ValueError(f"Duplicated SoC: {soc_name}")
        socs.append(soc_name)


def test_for_unknown_implementer():

    for soc in tables.socs:
        for core in soc["cores"]:
            try:
                if tables.cpu_cores[core["implementer"]]:
                    pass
            except KeyError:
                raise ValueError(
                    f"Missing {hex(core['implementer'])} core"
                    " implementer!",
                )


def test_for_unknown_core():

    for soc in tables.socs:
        for core in soc["cores"]:
            core_prv = f'{hex(core["part"])}-{core["revision"]}-' \
                f'{core["variant"]}'
            try:
                if tables.cpu_cores[core["implementer"]]["cores"][
                        core_prv]:
                    pass
            except KeyError:
                try:
                    if tables.cpu_cores[core["implementer"]]["cores"][
                            hex(core["part"])]:
                        pass
                except KeyError:
                    raise ValueError(
                        f"Missing data for {hex(core['part'])} core for "
                        f"{hex(core['implementer'])}!",
                    )


def test_for_unknown_feature():

    for soc in tables.socs:
        for feature in soc["features"]:
            try:
                if tables.cpu_features[feature]:
                    pass
            except KeyError:
                soc_name = f"{soc['vendor']}:{soc['name']}"
                raise ValueError(f"Unknown cpu feature '{feature}' "
                                 f"in {soc_name}")
