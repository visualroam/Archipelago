from typing import Dict, Set

from .names import region_names as rname

REPO_regions: Dict[str, Set[str]] = {
    rname.menu: {
        rname.shop,
        rname.headman,
        rname.mcjannek,
        rname.swiftbroom,
        rname.museum,
        rname.sunstone
    },
    rname.shop: set(),
    rname.headman: set(),
    rname.mcjannek: set(),
    rname.swiftbroom: set(),
    rname.museum: set(),
    rname.sunstone: set()
}

