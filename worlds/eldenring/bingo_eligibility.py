"""Goal exclusions shared by the world and standalone host importer (no AP imports)."""


def crafting_goal(label):
    """Crafting needs recipe/container/material supply and action provenance together."""
    return label.strip().casefold().split(maxsplit=1)[0:1] == ["craft"]
