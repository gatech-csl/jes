# pixel-benchmarks.py
# Runs a bunch of tests involving pixels,
# so you can gauge the speed of user code.
import sys
from jes.extras import callAndTime
from media import *
from os.path import basename

benchmarks = []

def benchmark(fn):
    benchmarks.append(fn)
    return fn


@benchmark
def loopManuallyNop(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)


@benchmark
def loopManuallyGetColor(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            getColor(pix)


@benchmark
def loopManuallyGetOneChannel(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            getRed(pix)


@benchmark
def loopManuallyGetThreeChannels(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            getRed(pix)
            getGreen(pix)
            getBlue(pix)


@benchmark
def loopManuallySetColor(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            setColor(pix, white)


@benchmark
def loopManuallySetOneChannel(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            setRed(pix, 255)


@benchmark
def loopManuallySetThreeChannels(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            setRed(pix, 255)
            setGreen(pix, 255)
            setBlue(pix, 255)


@benchmark
def loopManuallyScaleColor(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            color = getColor(pix)
            setColor(pix, makeColor(
                color.getRed() / 2, color.getGreen() / 2, color.getBlue() / 2
            ))


@benchmark
def loopManuallyScaleOneChannel(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            setRed(pix, getRed(pix) / 2)


@benchmark
def loopManuallyScaleThreeChannels(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            setRed(pix, getRed(pix) / 2)
            setGreen(pix, getGreen(pix) / 2)
            setBlue(pix, getBlue(pix) / 2)


@benchmark
def loopManuallyLighten(pic):
    for y in range(getHeight(pic)):
        for x in range(getWidth(pic)):
            pix = getPixel(pic, x, y)
            setColor(pix, makeLighter(getColor(pix)))


@benchmark
def loopOverPixArrayNop(pic):
    for pix in getPixels(pic):
        pass


@benchmark
def loopOverPixArrayGetColor(pic):
    for pix in getPixels(pic):
        getColor(pix)


@benchmark
def loopOverPixArrayGetOneChannel(pic):
    for pix in getPixels(pic):
        getRed(pix)


@benchmark
def loopOverPixArrayGetThreeChannels(pic):
    for pix in getPixels(pic):
        getRed(pix)
        getBlue(pix)
        getGreen(pix)


@benchmark
def loopOverPixArraySetColor(pic):
    for pix in getPixels(pic):
        setColor(pix, white)


@benchmark
def loopOverPixArraySetOneChannel(pic):
    for pix in getPixels(pic):
        setRed(pix, 255)


@benchmark
def loopOverPixArraySetThreeChannels(pic):
    for pix in getPixels(pic):
        setRed(pix, 255)
        setGreen(pix, 255)
        setBlue(pix, 255)


@benchmark
def loopOverPixArrayScaleColor(pic):
    for pix in getPixels(pic):
        color = getColor(pix)
        setColor(pix, makeColor(
            color.getRed() / 2, color.getGreen() / 2, color.getBlue() / 2
        ))


@benchmark
def loopOverPixArrayScaleOneChannel(pic):
    for pix in getPixels(pic):
        setRed(pix, getRed(pix) / 2)


@benchmark
def loopOverPixArrayScaleThreeChannels(pic):
    for pix in getPixels(pic):
        setRed(pix, getRed(pix) / 2)
        setGreen(pix, getGreen(pix) / 2)
        setBlue(pix, getBlue(pix) / 2)


@benchmark
def loopOverPixArrayLightenColor(pic):
    for pix in getPixels(pic):
        setColor(pix, makeLighter(getColor(pix)))


def runBenchmarks(filenames):
    warmedUp = False

    for filename in filenames:
        print >>sys.stderr, "== Benchmarks for %s ==" % basename(filename)

        pic = callAndTime(makePicture, filename)
        print >>sys.stderr, pic
        print >>sys.stderr

        if not warmedUp:
            # Warm up. On the first round, some Java classes still haven't been
            # loaded, so the first benchmark takes a hit.
            loopManuallyGetColor(pic)
            warmedUp = True

        for benchmark in benchmarks:
            # We create a fresh picture on each benchmark,
            # to invalidate any caches.
            pic = makePicture(filename)
            callAndTime(benchmark, pic)

        print >>sys.stderr


if __name__ == '__main__':
    runBenchmarks(sys.argv[1:])

