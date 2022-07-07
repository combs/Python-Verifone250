from __future__ import print_function
import serial,time

ESCAPE=chr(27)
red="red"
black="black"

class Verifone250(object):

    # from Verifone250 import Verifone250
    # v = Verifone250(port="/dev/cu.wchusbserial110")

    # v = Verifone250(port="/dev/cu.wchusbserial110",DEBUG_Remote=True,
    # speed=9600, bytesize=Serial.SEVENBITS, parity=serial.PARITY_EVEN,
    # autoReset = True)



    # Do we reset formatting after every print command?
    # Or let it carry over, per printer's idiosyncratic logic:

    autoReset = True

    # Seven-bit mode is required for double wide printing.
    # Eight-bit mode allows for more characters.
    # Set per DIP switches inside ribbon area

    bytesize=serial.SEVENBITS

    # Do we spew a lot of debug via print()?

    DEBUG_Remote = False

    # Is the printer currently in doubleWide or doubleTall mode?

    doubleWide = False
    doubleTall = False

    # Is the printer in "Printer 200 Emulation Mode" or "Native Mode"?
    # Native mode is required for all escape sequences.

    nativeMode = False

    # Set per DIP switches inside ribbon area

    parity=serial.PARITY_EVEN

    # Serial port to which the Verifone250 is attached

    port = ""

    # Is the printer currently in black or red mode?

    isRed = False

    # Any extra junk to pass to pyserial?

    serialParameters = {}

    # Set per DIP switches inside ribbon area

    speed = 9600

    # Printer supports hardware handshakes instead of just blindly waiting,
    # but none of my other equipment supports this :P
    # so we accumulate delay at an estimated rate and wait for it when printing.

    timePending = 0.0

    # Serial timeouts. Really only matters for reads

    timeout=5
    write_timeout=None

    def __init__(self, *args, **kwargs):

        # Flags

        if type (args) is not None:
            for arg in args:
                setattr(self,key,True)

        # key=value parameters

        if type (kwargs) is not None:
            for key, value in kwargs.items():
                if type(value) is dict:
                    if getattr(self,key):
                        tempdict = getattr(self,key).copy()
                        tempdict.update(value)
                        value = tempdict
                setattr(self,key,value)

        self.ser = serial.Serial(self.port, self.speed, bytesize=self.bytesize, parity=self.parity, timeout=self.timeout, write_timeout=self.write_timeout, **self.serialParameters)

        if self.DEBUG_Remote:
            print(str(self.ser.get_settings()))

        self.softReset()


    def bufferChars(self,stuff):
        # DIY

        self.ser.write(stuff)

    def eject(self,lines=1):
        # Yack out some paper! Max 10 lines

        self.enterNativeMode()
        self.remoteWrite(ESCAPE,'b',str(int(lines % 10)),';')
        time.sleep(0.4 * int(lines % 10))

    def enterDoubleWideMode(self):
        # Double wide mode can be mixed and matched in a single line.

        if self.doubleWide:
            return
        self.enterNativeMode()
        self.doubleWide = True
        self.remoteWrite(chr(30))

    def exitDoubleWideMode(self):
        if self.doubleWide:
            self.doubleWide = False
            self.remoteWrite(chr(31))

    def enterDoubleTallMode(self):
        # Double tall mode is line at a time.
        # If you send a line in multiple chunks, it goes by
        # what's set at newline time

        if self.doubleTall:
            return
        self.enterNativeMode()
        self.doubleTall = True
        self.remoteWrite(ESCAPE,'f',chr(49),chr(49),';')

    def exitDoubleTallMode(self):
        if self.doubleTall:
            self.doubleTall = False
            self.remoteWrite(ESCAPE,'f',chr(48),chr(48),';')

    def enterNativeMode(self):
        # Entering native mode flushes the buffer, so we try to avoid it:
        if self.nativeMode:
            return

        self.remoteWrite(chr(0x1C))
        self.nativeMode = True
        self.__clearFormatting()

    def __clearFormatting(self):

        # Internal helper. Doesn't write anything to printer

        self.doubleTall = False
        self.doubleWide = False
        self.isRed = False

    def exitNativeMode(self):

        # This is the same as "Enter Printer 200 Emulation Mode"

        # Exiting native mode flushes the buffer, so we try to avoid it:
        if self.nativeMode:
            self.remoteWrite(chr(0x1D))
            self.nativeMode = False

        return

        self.__clearFormatting()


    def flushBuffer(self):
        # Newline

        self.remoteWrite(chr(10))

    def __formatRemoteValues(self,values):
        # A pretty printer for debug output

        returnValue=""
        for a in values:
            if (type(a) is int):
                if (a > 31 and a < 127):
                    returnValue = returnValue + "'" + str(a) + "' (" + str(a) + "), "
                else:
                    returnValue = returnValue + "(" + str(a) + "), "
            elif (type(a) is str):
                if ((ord(a) > 31 ) and ( ord(a) < 127)):
                    returnValue = returnValue + "'" + str(a) + "' (" + str(ord(a)) + "), "
                else:
                    returnValue = returnValue + "(" + str(ord(a)) + "), "
        return returnValue

    def getBytes(self,number):
        # Only a few functions require this
        return self.ser.read(number)

    def getPrinterStatus(self):

        # The commands retrieving data from the printer all fail on mine.
        # I'm not sure if this is a problem in the code or the hardware.
        # Let me know if you get this to work.
        # https://github.com/combs/Python-Verifone250/issues/1

        self.remoteWrite(ESCAPE,chr(0x64))

        rawVal = self.getBytes(1)

        if len(rawVal) > 0:
            rawVal = rawVal[0]
        else:
            if self.DEBUG_Remote:
                print("Timed out waiting for getPrinterStatus.")
            return {"timeout": True}

        returnVals = {}
        returnVals["raw"] = rawVal
        returnVals["paperLow"] = rawVal & 1
        returnVals["alwaysHigh"] = rawVal & 32
        returnVals["mechanismFailure"] = rawVal & 64
        returnVals["timeout"] = False
        return returnVals

    def identifyPrinter(self):

        # The commands retrieving data from the printer all fail on mine.
        # I'm not sure if this is a problem in the code or the hardware.
        # Let me know if you get this to work.
        # https://github.com/combs/Python-Verifone250/issues/1

        self.remoteWrite(ESCAPE,'i')
        rawVal = self.getBytes(1)

        if len(rawVal) > 0:
            rawVal = rawVal[0]
            return rawVal
        else:
            if self.DEBUG_Remote:
                print("Timed out waiting for identifyPrinter.")
            return

    def printChars(self,stuff,**kwargs):

        # Queue up some characters in the buffer.
        # v.printChars("text",color="red",doubleWide=False,doubleTall=True,autoReset=True)

        autoReset = kwargs.get("autoReset", self.autoReset)
        
        if autoReset:
            self.exitDoubleTallMode()
            self.exitDoubleWideMode()
            self.setBlack()

        if kwargs.get("doubleTall", False):
            self.enterDoubleTallMode()
        else:
            self.exitDoubleTallMode()

        if kwargs.get("doubleWide", False):
            self.enterDoubleWideMode()
        else:
            self.exitDoubleWideMode()

        if kwargs.get("color", "black") == "red":
            self.setRed()
        else:
            self.setBlack()

        self.remoteWrite(*stuff)

    def printLine(self,stuff,**kwargs):
        # Recommended way to tee stuff up unless you need to mix and match
        # colors/widths in one line.
        # v.printLine("text",color="red",doubleWide=False,doubleTall=True,autoReset=True)

        self.printChars(stuff,**kwargs)

        self.flushBuffer()

    def remoteWrite(self,*values):
        # Dump some raw stuff to the printer.
        # v.remoteWrite('c',chr(50),chr(0x38), etc)

        if self.DEBUG_Remote:
            print("-> " + self.__formatRemoteValues(values))

        converted = bytearray()
        for val in values:
            if type(val)==str:
                converted += converted.encode('ascii')
            else:
                converted += val

        for theByte in theBytes:
            self.ser.write([theByte])
            time.sleep( 1 / self.speed * 2 )

            if self.DEBUG_Remote:
                print("waiting for flush", end="")

            # realistically a usb serial has its own weird magical buffer, so
            # the kernel's idea of whether this serial buffer is empty is a bit
            # hooey. But hey, let's honor it if possible

            while (self.ser.out_waiting):
                time.sleep(0.0001)
                if self.DEBUG_Remote:
                    print('.', end="")
            if self.DEBUG_Remote:
                print(" ")

            if theByte==10:

                # Newline, triggers printer to print its buffer.

                # The printer resets to black every line :P

                self.isRed = False
                self.timePending += 0.2
                if self.doubleTall:
                    self.timePending *= 2

                if self.DEBUG_Remote:
                    print("Pausing for",self.timePending,"seconds")

                time.sleep(self.timePending)

                self.timePending = 0.0

            else:
                # Let's guess 0.03 seconds per character
                self.timePending += 0.03

                if self.doubleWide:
                    self.timePending += 0.03
                    # do it double



    def retrievePrinterInformation(self):

        # The commands retrieving data from the printer all fail on mine.
        # I'm not sure if this is a problem in the code or the hardware.
        # Let me know if you get this to work.
        # https://github.com/combs/Python-Verifone250/issues/1

        self.remoteWrite(ESCAPE, chr(0x72), '0')

        # TODO: retrieve the bytes. How are they delimited?

    def softReset(self):

        self.nativeMode = False
        self.enterNativeMode()
        self.remoteWrite(ESCAPE,'c')
        self.nativeMode = False
        self.__clearFormatting()

    def swapColor(self):
        # Instead of just having a "red" or "black" command, the printer has a
        # "toggle" escape sequence. So we hang on to a local idea of what it is
        # set to, and then update the printer as needed.

        # BTW, the printer resets this every line, just for lullz

        self.isRed = not (self.isRed)
        self.remoteWrite(chr(18))

    def setColor(self,red=False):
        # Just convenience stuff

        if red is self.isRed:
            return
        else:
            self.swapColor()

    def setRed(self):
        # Just convenience stuff

        self.setColor(red=True)

    def setBlack(self):
        # Just convenience stuff

        self.setColor(red=False)
