# main doesnt do much right now
# just hard coding a selection of one of a couple patternAnimations to run



import time
from triangles.Node.nodeTime import *
from triangles.Animations.triangleAnimationResult import *
import patterns.patternAnimations as patternAnimations
from rpi_ws281x import *
from triangles.Node.triangleNode import *
import stripConfig as stripConfig
import argparse
import triangles.Animations.triangleAnimations as triangleAnimations

def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    return parser.parse_args()

    # print ('Press Ctrl-C to quit.')
    # if not args.clear:
    #     print('Use "-c" argument to clear LEDs on exit')

def doIndividualTesting():
    # use me to test things

    args = argParser()

    try:
        myPattern = patternAnimations.Testing()
        while True:
           myPattern.run()

    except KeyboardInterrupt:
        if args.clear:
            myPattern.clear()

def doRandomTemporarySwitcher():
    # this one works pretty well, no plans for improvement atm

    args = argParser()

    try:
        # divisors are so the lights dont saturate webcams, tune for your conditions
        divisorBackground = 20
        divisorSpecial = 20

        colorBackground = Color(255//divisorBackground, 0, 0)
        colorSpecial = Color(0, 0, 255//divisorSpecial)

        myPattern = patternAnimations.RandomTemporarySwitcher(colorBackground = colorBackground, colorSpecial = colorSpecial)

        while True:
           myPattern.run()
           
    except KeyboardInterrupt:
        if args.clear:
            myPattern.clear()

def doRandomizingWipe():
    # this one is in development, general idea works...
    # todo: timing is broken...phaser is doing strange stuff when switching colors...would like successive phaser colors to guarantee contrast

    args = argParser()

    try:
        # divisors are so the lights dont saturate webcams, tune for your conditions (this divisor isn't carried into future phaser colors...todo: send the divisor into the constructor???)
        divisorBackground = 50

        colorBackground = Color(255//divisorBackground, 0, 0)

        myPattern = patternAnimations.RandomizingWipe(colorStart = colorBackground)

        while True:
            myPattern.run()
           
    except KeyboardInterrupt:
        if args.clear:
            myPattern.clear()

def main():
    # just pick here which pattern to run
    # doRandomizingWipe()
    doRandomTemporarySwitcher()

main()
