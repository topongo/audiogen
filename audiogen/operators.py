import math
from . import generators
from . import util

MAX_MEM = 5 * pow(10, 8)


class PossibleMemoryOutage(Exception):
    pass


def oper(f1, f2, operand):
    period = abs(len(f1) * len(f2)) // math.gcd(len(f1), len(f2))
    if period * 24 > MAX_MEM:
        raise PossibleMemoryOutage("Warning: ONE variable was about to allocate more than " + str(MAX_MEM) + " bytes!")
    res = []
    ind = [0, 0]
    funcs = [f1, f2]
    for i in range(period):
        res.append({
                       "+": f1[ind[0]] + f2[ind[1]],
                        "-": f1[ind[0]] - f2[ind[1]],
                        "*": f1[ind[0]] * f2[ind[1]],
                        "/": f1[ind[0]] / (f2[ind[1]] + 0.0000000000000000000000001)  # avoiding dividing by zero
                    }[operand])
        for i in range(len(funcs)):
            if ind[i] >= len(funcs[i]) - 1:
                ind[i] = 0
            else:
                ind[i] += 1


    return res


def flat(f, fraction=1, offset=0):
    start_point = int(float(len(f)) * fraction)
    stop_point = int((float(len(f)) * offset) + start_point)
    if stop_point > len(f) - 1:
        stop_point = -1
    for i in range(len(f[start_point:stop_point])):
        f[i + start_point] = 0
    return f


def blink(f, freq=0.5):
    return oper(f, generators.saw(freq, tozero=True), "*")


def vol(gen, volume=100):
    volume = float(100) / volume
    return util.normalize_dict(gen, volume, -volume)
