# Python-Verifone250
A Python driver for the [Verifone 250](http://www.ebay.com/sch/Printers/46712/i.html?_from=R40&_nkw=verifone+250) serial receipt printer. Supports extended font goodies!

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

## Not yet implemented

- Port location/probing
- Reading anything from the printer... there's code for it in the library, but it does not function on my printer.
- Non-English charset
- Custom character downloads
- Graphical printing (the holy grail, but a pain, the printer requires a weird 6-bit format)
- Right margin
- Text centering via `textwrap` module

Pull requests are welcomed!


## Hardware

You'll need to hook up your Verifone 250 to some sort of serial interface. It has a Mini-DIN8 (round) serial connector. I have mine hooked up through a [Mini-DIN8 to DB9F adapter cable](http://www.ebay.com/sch/i.html?_from=R40&_trksid=p2047675.m570.l1313.TR0.TRC8.A0.H0.X%22DB9P+to+8P+Mini+Din+RS232+Cable+White%22.TRS5&_nkw=%22DB9P+to+8P+Mini+Din+RS232+Cable+White%22&_sacat=0), a [DB9M-DB9M gender changer](http://www.ebay.com/sch/i.html?_odkw=DB9+Male+Serial+Cable+Gender+Changer&_osacat=0&_from=R40&_trksid=m570.l1313&_nkw=DB9+Male+Serial+Gender+Changer&_sacat=0), a [DB9F to TTL serial adapter](http://www.ebay.com/sch/i.html?_odkw=db9%20ttl&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR10.TRC2.A0.H0.Xdb9+ttl.TRS2&_nkw=db9+ttl&_sacat=0) (make sure to get one that includes jumper wires if you don't have any), and finally a [USB to TTL serial adapter](http://www.ebay.com/sch/i.html?_odkw=usb+ttl&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.A0.H0.Xusb+ttl.TRS1&_nkw=usb+ttl&_sacat=0).

Note that there are about a gazillion different internal wirings for Mini-DIN8 to DB9 cables. I just lucked on the right one by buying a few. 

When you're first trying out an unproven Mini-DIN8 to DB9 cable, keep an eye out for extra heat coming from any of your equipment, LEDs suddenly dimming when you plug the last part in, computer complaining about USB power consumption...  any of that stuff happens, yank out the plug and try another. 

Many of the cheapest USB to TTL serial adapters require a driver on Mac OS X. CP2102, CH340, etc. 

## About the printer

It uses ink ribbons and boring, non-thermal paper in 3" rolls.

There are four DIP switches hidden under the right side of the ink ribbon. They control its serial connectivity settings. See [reference guide](https://github.com/combs/Python-Verifone250/files/907688/Verifone.250.pdf).

There is a silly "paper level" sensor that just uses IR light reflectivity. If you leave off the paper cover, the sensor will get tricked by any ambient light.

The AC adapter is huge and funky, don't buy a printer without it. It feeds the printer 22V AC @ 1.5A (yes really)

I haven't had much luck finding TTL serial signals on the printer's board, but surely it's possible, right? Let me know if you do!!


## More usage info

The [library itself](https://github.com/combs/Python-Verifone250/blob/master/Verifone250.py) describes the individual functions in more detail.

Or check out the printer's [reference guide](https://github.com/combs/Python-Verifone250/files/907688/Verifone.250.pdf).
