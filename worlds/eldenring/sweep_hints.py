"""Seed-specific sweep instructions, separate from the shared AP location names."""
import re

_CLAUSE = re.compile(r", (?:may be sweep-granted by|also granted by) .*?(?= \[f\d+\]$|$)")


def location_name(name):
    """Keep the pickup description and acquisition identity, without a corpus-wide promise."""
    return _CLAUSE.sub("", name)


def data_package(package):
    """Publish clean names without mutating the world's internal names or shared group lists."""
    from worlds.AutoWorld import data_package_checksum
    names = {location_name(name): aid for name, aid in package["location_name_to_id"].items()}
    if len(names) != len(package["location_name_to_id"]):
        raise ValueError("Removing sweep descriptions collided two AP location names")
    result = {key: value for key, value in package.items() if key != "checksum"}
    result["location_name_to_id"] = names
    result["location_name_groups"] = {
        group: sorted(location_name(name) for name in members)
        for group, members in package["location_name_groups"].items()
    }
    result = dict(sorted(result.items()))
    result["checksum"] = data_package_checksum(result)
    return result


def instructions(locations, candidates, sweeps, bosses):
    """Use the final emitted sweep groups; other players' settings never enter this mapping."""
    by_location = {}
    for trigger, members in sweeps.items():
        info = bosses.get(int(trigger))
        label = info[3].strip() if info and len(info) > 3 else ""
        label = "Swept by " + label if label else "Collected by an area sweep"
        for aid in members:
            by_location.setdefault(aid, set()).add(label)
    return {
        aid: "; ".join(sorted(by_location[aid])) if aid in by_location else "Manual pickup"
        for aid in locations if aid in candidates or aid in by_location
    }
