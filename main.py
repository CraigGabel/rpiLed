import time
import individualTest
from nodeTime import *
from nodeResult import *
import patternAnimations
from rpi_ws281x import *
from triangleNode import *
from ledAnimations import *
import stripConfig as stripConfig
import argparse
import triangleAnimations

def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    return parser.parse_args()

    # print ('Press Ctrl-C to quit.')
    # if not args.clear:
    #     print('Use "-c" argument to clear LEDs on exit')

def main():

    args = argParser()

    try:
       
        myTimer = NodeTime(True)

        # individual testing
        # myPattern = individualTest.IndividualTest()
        myPattern = patternAnimations.Testing()
        while True:
           myPattern.run()


        # ## incrementing switcher
        # divisor = 50
        # colors = [Color(255//divisor, 0, 0), Color(0, 255//divisor, 0), Color(0, 0, 255//divisor)]
        # colorIndex = 0
        # modes = [triangleAnimations.Wipe, triangleAnimations.SingleCircle]
        # modeIndex = 0
        # myPattern = patternAnimations.IncrementingColorSwitch(strip=None, switcherMode=modes[modeIndex], switcherColor=colors[colorIndex])

        # while True:
        #     result = myPattern.run()
        #     if (result):
        #         colorIndex = (colorIndex + 1) % len(colors)
        #         modeIndex = (modeIndex + 1) % len(modes)
        #         myPattern = patternAnimations.IncrementingColorSwitch(strip=myPattern.strip, switcherMode=modes[modeIndex], switcherColor=colors[colorIndex])

        ## phaser show
        divisorBackground = 50
        divisorSpecial = 50
        # colorBackground = Color(83//divisorBackground, 30//divisorBackground, 232//divisorBackground)
        # colorSpecial = Color(232//divisorSpecial, 201//divisorSpecial, 30//divisorSpecial)
        colorBackground = Color(255//divisorBackground, 0, 0)
        colorSpecial = Color(0, 0, 255//divisorSpecial)
        # myPattern = patternAnimations.MjlShow(colorBackground = colorBackground, colorSpecial = colorSpecial)
        # myPattern = patternAnimations.RandomTemporarySwitcher(colorBackground = colorBackground, colorSpecial = colorSpecial)
        myPattern = patternAnimations.RandomizingWipe(colorStart = colorBackground)

        while True:
            myPattern.run()

    except KeyboardInterrupt:
        if args.clear:
            myPattern.clear()

main()
