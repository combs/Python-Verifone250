# Python-Verifone250
A Python driver for the serial receipt printer Verifone 250. Supports extended font goodies 🆎  🆔  № 💯 

![Sample output](https://cloud.githubusercontent.com/assets/6174018/24831029/ba3fd5a8-1c5f-11e7-8ad5-29dac0bd8989.jpg)

## Usage

```
from Verifone250 import Verifone250

v = Verifone250(port="/dev/cu.wchusbserial110")

v.printLine("My first line!")

v.printLine("Red and big",color="red",doubleWide=True,doubleTall=True)

v.printLine("Black and small",color="black",doubleWide=False,doubleTall=False)

v.printChars("Red part of a line",color="red")
v.printLine(" and black part",color="black")


```
## Hardware

You'll need to hook up your Verifone 250 to some sort of serial interface. It has a Mini-DIN8 (round) serial connector. I have mine hooked up through a Mini-DIN8 to DB9F adapter, a DB9M-DB9M gender changer, a DB9F to TTL serial adapter, and finally a USB to TTL serial adapter.

## More usage info

The [library itself](https://github.com/combs/Python-Verifone250/blob/master/Verifone250.py) describes the individual functions in more detail.

Or check out the printer's reference guide: [Verifone 250.pdf](https://github.com/combs/Python-Verifone250/files/907688/Verifone.250.pdf)
