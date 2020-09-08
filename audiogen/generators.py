# coding=utf8

'''
Assorted generators 
'''

import math
import itertools

from . import util
from . import sampler

TWO_PI = 2 * math.pi


## Audio sample generators

def sin(freq=440, min_=-1, max_=1):
    period = int(sampler.FRAME_RATE / freq)
    time_scale = 2 * math.pi / period  # period * scale = 2 * pi
    # precompute fixed tone samples # TODO: what about phase glitches at end?
    return [math.sin(i * time_scale) for i in range(period)]


def cos(freq=440, min_=-1, max_=1):
    period = int(sampler.FRAME_RATE / freq)
    time_scale = 2 * math.pi / period  # period * scale = 2 * pi
    # precompute fixed tone samples # TODO: what about phase glitches at end?
    return [math.cos(i * time_scale) for i in range(period)]


def square(freq, reverse=False):
    period = int(sampler.FRAME_RATE / freq)
    # time_scale = 2 * math.pi / period
    # period * scale = 2 * pi
    # precompute fixed tone samples # TODO: what about phase glitches at end?
    return [(1 if i >= period / 2 else -1) * (-1 if reverse else 1) for i in range(period)]


def saw(freq, reverse=False, tozero=False):
    period = int(sampler.FRAME_RATE / freq)
    # time_scale = 2 * math.pi / period
    # period * scale = 2 * pi
    # precompute fixed tone samples # TODO: what about phase glitches at end?
    return [((1 if tozero else 2) * (float(i) / period) - (0 if tozero else 1)) * (-1 if reverse else 1) for i in
            range(period)]


# while True:
#	for i in xrange(period):
#		yield samples[i]

def silence(seconds=None):
    if seconds != None:
        for i in range(int(sampler.FRAME_RATE * seconds)):
            yield 0
    else:
        while True:
            yield 0


def gen(samp, volume):
    volume = float(100) / volume
    while True:
        for i in range(len(util.normalize(gen, volume, -volume))):
            yield samp[i]
