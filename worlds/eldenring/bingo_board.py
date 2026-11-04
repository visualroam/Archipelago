"""Pure board decisions. AP IDs below reserve new synthetic locations, never game flags."""
import hashlib
import random

BINGO_LOCATION_BASE = 7786000
MIN_BOARD_SIZE = 5
MAX_BOARD_SIZE = 12
LOCATION_NAMES = {f"Bingo Square {i + 1:02d}": BINGO_LOCATION_BASE + i for i in range(MAX_BOARD_SIZE ** 2)}


def board_area(size=5):
    if type(size) is not int or not MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE:
        raise ValueError("bingo_board_size must be an integer from 5 to 12")
    return size * size


def lines(size=5):
    board_area(size)
    return (tuple(tuple(r * size + c for c in range(size)) for r in range(size)) +
            tuple(tuple(r * size + c for r in range(size)) for c in range(size)) +
            (tuple(i * (size + 1) for i in range(size)),
             tuple((i + 1) * (size - 1) for i in range(size))))


LINES = lines()


def has_line(done, size=5):
    if len(done) != board_area(size):
        raise ValueError("bingo completion cells do not match board dimensions")
    return any(all(done[i] for i in line) for line in lines(size))


def is_complete(done, goal, count, size=5):
    area = board_area(size)
    if len(done) != area:
        raise ValueError("bingo completion cells do not match board dimensions")
    return has_line(done, size) if goal == "line" else sum(done) >= (area if goal == "blackout" else count)


def select_board(candidates, seed, *, region_limit=None, parents=None, start_pool=(), starts=1, size=5):
    """Separate RNG; stable candidates and unique encounter flags, independent of fill calls."""
    area = board_area(size)
    candidates = sorted(candidates, key=lambda c: c["flag"])
    if len({c["flag"] for c in candidates}) != len(candidates):
        raise ValueError("bingo candidate encounter flags must be unique")
    if len(candidates) < area:
        raise ValueError(f"bingo needs {area} eligible boss encounters; only {len(candidates)} remain")
    rng = random.Random(hashlib.sha256(str(seed).encode()).digest())
    if region_limit is None:
        selected = rng.sample(candidates, area)
    else:
        parents = parents or {}
        def closure(region):
            result = {region}
            while region in parents:
                region = parents[region]
                if region in result:
                    raise ValueError("bingo region parents contain a cycle")
                result.add(region)
            return result
        for _attempt in range(128):
            order = rng.sample(candidates, len(candidates))
            opening = []
            if start_pool:
                for cell in order:
                    if cell["region"] in start_pool and cell["region"] not in {c["region"] for c in opening}:
                        opening.append(cell)
                        if len(opening) == starts:
                            break
                if len(opening) < starts:
                    raise ValueError("bingo start_region_pool needs enough distinct regions with eligible objectives")
            selected, regions = [], set()
            for cell in opening + [c for c in order if c not in opening]:
                needed = regions | closure(cell["region"])
                if len(needed) <= region_limit:
                    selected.append(cell)
                    regions = needed
                if len(selected) == area:
                    break
            if len(selected) == area and all(c in selected for c in opening):
                rng.shuffle(selected)
                break
        else:
            raise ValueError(f"bingo cannot fit {area} objectives in {region_limit} regions; increase bingo_region_limit")
    return [dict(c, location=BINGO_LOCATION_BASE + i) for i, c in enumerate(selected)]
