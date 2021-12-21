
from typing import Iterator

from common import problem_data

class BitStream:
    @staticmethod
    def _bitstream(hex_str: str) -> Iterator[str]:
        for h in hex_str:
            yield from format(int(h, base=16), "04b")

    def __init__(self, hex_str: str):
        self._last_read = -1
        self._stream = self._bitstream(hex_str)

    def __iter__(self):
        return self

    def __next__(self):
        bit = next(self._stream)
        self._last_read += 1
        return bit

    def state(self):
        return self._last_read

    def str_(self, len_: int) -> str:
        return "".join(next(self) for _ in range(len_))

    def num(self, len_: int) -> int:
        return int(self.str_(len_), base=2)


def header(bits: BitStream) -> tuple[int, int]:
    version = bits.num(3)
    type_ = bits.num(3)
    return (version, type_)

def literal(bits: BitStream) -> int:
    bin_str = []
    while (prefix := bits.str_(1)) != "0":
        bin_str.append(bits.str_(4))
    bin_str.append(bits.str_(4))
    return int("".join(bin_str), base=2)

class Packet:
    version: int
    type_: int

    def __init__(self, version, type_):
        self.type_ = type_
        self.version = version


    def __repr__(self):
        return f"Packet({self.version}, {self.type_})"

    @staticmethod
    def literal(version, type_, number):
        p = Packet(version, type_)
        p.number = number
        return p

    @staticmethod
    def operator(version, type_, packets):
        p = Packet(version, type_)
        p.packets = packets
        return p


def operator_packets(bits: BitStream) -> list[Packet]:
    length_id = bits.str_(1)
    if length_id == "0":
        bit_count = bits.num(15)
        stop_state = bits.state() + bit_count
        packets = []
        while bits.state() < stop_state:
            packets.append(packet(bits))
        if bits.state() != stop_state:
            raise Exception("Inconsistent read state")
    else:
        packet_count = bits.num(11)
        packets = [packet(bits) for _ in range(packet_count)]
    return packets


def packet(bits: BitStream) -> Packet:
    version, type_ = header(bits)
    if type_ == 4:
        return Packet.literal(version, type_, literal(bits))
    else:
        return Packet.operator(version, type_, operator_packets(bits))


def versions(packet: Packet) -> list[int]:
    if getattr(packet, "packets", None) is None:
        return [packet.version]
    else:
        versions_ = [packet.version]
        for p in packet.packets:
            versions_.extend(versions(p))
        return versions_


sample_data = problem_data("day16_sample1.txt")
print(sum(versions(packet(BitStream(next(sample_data))))))
print(sum(versions(packet(BitStream(next(sample_data))))))
print(sum(versions(packet(BitStream(next(sample_data))))))
print(sum(versions(packet(BitStream(next(sample_data))))))

print(sum(versions(packet(BitStream(next(problem_data("day16_problem.txt")))))))

def eval_(packet: Packet) -> int:
    if packet.type_ == 4:
        return packet.number
    elif packet.type_ == 0:
        return sum(eval_(p) for p in packet.packets)
    elif packet.type_ == 1:
        mult = 1
        for p in packet.packets:
            mult *= eval_(p)
        return mult
    elif packet.type_ == 2:
        return min(eval_(p) for p in packet.packets)
    elif packet.type_ == 3:
        return max(eval_(p) for p in packet.packets)
    elif packet.type_ == 5:
        assert len(packet.packets) == 2
        if eval_(packet.packets[0]) > eval_(packet.packets[1]):
            return 1
        else:
            return 0
    elif packet.type_ == 6:
        assert len(packet.packets) == 2
        if eval_(packet.packets[0]) < eval_(packet.packets[1]):
            return 1
        else:
            return 0
    elif packet.type_ == 7:
        assert len(packet.packets) == 2
        if eval_(packet.packets[0]) == eval_(packet.packets[1]):
            return 1
        else:
            return 0

sample_data = problem_data("day16_sample2.txt")
print(eval_(packet(BitStream(next(sample_data)))))
print(eval_(packet(BitStream(next(sample_data)))))
print(eval_(packet(BitStream(next(sample_data)))))
print(eval_(packet(BitStream(next(sample_data)))))
print(eval_(packet(BitStream(next(sample_data)))))
print(eval_(packet(BitStream(next(sample_data)))))
print(eval_(packet(BitStream(next(sample_data)))))
print(eval_(packet(BitStream(next(sample_data)))))

print(eval_(packet(BitStream(next(problem_data("day16_problem.txt"))))))
