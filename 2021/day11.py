from __future__ import annotations

from common import ordered_intmap

# Solution is insane, don't do it again - but steps are a bit cheaper!
class OctoMap:
    class Octopus:
        band: EnergyBand
        neighbours: frozenset[Octopus]
        pos: tuple[int, int]

        def __init__(self, band: OctoMap.EnergyBand, pos: tuple[int, int]):
            self.band = band
            self.pos = pos

        def __repr__(self):
            return f"Octo({self.pos})"

    class EnergyBand:
        next_: EnergyBand
        prev: EnergyBand
        octopi: set[Octopus]

        def __init__(self):
            self.octopi = set()

        @staticmethod
        def looped_set(size: int) -> frozenset[OctoMap.EnergyBand]:
            bands = [OctoMap.EnergyBand() for _ in range(size)]
            prev_band = None
            for i, band in enumerate(bands[:-1]):
                band.next_ = bands[i + 1]
                band.prev = prev_band
                prev_band = band
            bands[-1].next_ = bands[0]
            bands[-1].prev = prev_band
            bands[0].prev = bands[-1]
            return frozenset(bands)

        def __repr__(self):
            return f"EnergyBand({self.octopi})"

    bands: frozenset[OctoMap.EnergyBand]
    band_last: OctoMap.EnergyBand
    rows: int
    cols: int
    MAX_ENERGY: int = 10

    def __init__(self, map_data):
        # Energy level is stored in the linked list traversal
        # Storing band_last always lets us know where 9 is and we can
        # loop starting from there
        self.bands = OctoMap.EnergyBand.looped_set(self.MAX_ENERGY)
        self.band_last = next(iter(self.bands))

        numbered_bands = []
        band = self.band_last.next_
        for _ in range(self.MAX_ENERGY):
            numbered_bands.append(band)
            band = band.next_

        indexed_octopi = {}
        for y, x, energy in map_data:
            energy_band = numbered_bands[energy]
            octopus = OctoMap.Octopus(energy_band, (y, x))
            numbered_bands[energy].octopi.add(octopus)
            indexed_octopi[(y, x)] = octopus

        self.rows = y + 1
        self.cols = x + 1

        for (y, x), octopus in indexed_octopi.items():
            neighbours = set()
            for ystep in (-1, 0, 1):
                for xstep in (-1, 0, 1):
                    y2 = y + ystep
                    x2 = x + xstep

                    if -1 < y2 < self.rows and -1 < x2 < self.cols:
                        neighbours.add(indexed_octopi[(y2, x2)])
            octopus.neighbours = frozenset(neighbours)

    def step(self):
        # Step is done by decrementing the band_last pointer, and bumping neighbour
        # octopi into the next energy band
        flashing_band = self.band_last

        flashed_octopi = set()
        while len(flashing_band.octopi) > 0:
            flashing_octopus = flashing_band.octopi.pop()
            for neighbour in flashing_octopus.neighbours:
                if neighbour.band is not flashing_band:
                    next_band = neighbour.band.next_
                    neighbour.band.octopi.remove(neighbour)
                    next_band.octopi.add(neighbour)
                    neighbour.band = next_band
            flashed_octopi.add(flashing_octopus)
        flashing_band.octopi = flashed_octopi
        self.band_last = flashing_band.prev

        return len(flashed_octopi)


def count_octomap_flashes(octomap: OctoMap, steps: int):
    count = 0
    for _ in range(steps):
        count += octomap.step()
    return count

print(count_octomap_flashes(OctoMap(ordered_intmap("day11_sample.txt")), 100))
print(count_octomap_flashes(OctoMap(ordered_intmap("day11_problem.txt")), 100))

def run_until_synchronized(octomap: OctoMap):
    count = 1
    octopus_count = octomap.rows * octomap.cols
    while (octomap.step() != octopus_count):
        count += 1
    return count

print(run_until_synchronized(OctoMap(ordered_intmap("day11_sample.txt"))))
print(run_until_synchronized(OctoMap(ordered_intmap("day11_problem.txt"))))
