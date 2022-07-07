from __future__ import print_function

from time import sleep

from Verifone250 import Verifone250

v = Verifone250(port="/dev/ttyUSB0", DEBUG_Remote=True)



# The commands retrieving data from the printer all fail on mine.
# I'm not sure if this is a problem in the code or the hardware.
# Let me know if you get this to work.
# https://github.com/combs/Python-Verifone250/issues/1
#
# print(v.getPrinterStatus())
#
# print(v.retrievePrinterInformation())
#
# print(v.identifyPrinter())

v.eject(3)

# The most convenient for assembling a line at a time.

v.printLine("Red and big",color="red",doubleWide=True,doubleTall=True)
v.printLine("Black and small",color="black",doubleWide=False,doubleTall=False)


# Or you can handle all the mode toggling yourself
v.enterDoubleTallMode()
v.enterDoubleWideMode()
v.printLine("This is big",autoReset=False)

v.exitDoubleTallMode()
v.exitDoubleWideMode()

# Mixed colors in one line! Fancy!
v.setRed()
v.printChars("This makes your",autoReset=False)
v.setBlack()
v.printLine(" printer sound funny",autoReset=False)
v.flushBuffer()


v.enterDoubleWideMode()
v.printLine("Double wide ",autoReset=False)
v.exitDoubleWideMode()

v.enterDoubleTallMode()
v.setRed()
v.printLine("double tall",autoReset=False)
v.exitDoubleTallMode()

v.eject(3)
