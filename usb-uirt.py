#!/usr/bin/env python

import serial
import time
import sys
import os

DEBUG = True

# Response Codes
TRANSMITTING = 0x20
CMDOK = 0x21
CSERROR = 0x80   #Checksum Error
TOERROR = 0x81   #Timeout Error
CMDERROR = 0x82  #Command Error
# Command Codes
SETMODEUIR = 0x20
SETMODERAW = 0x21
SETMODERAW2 = 0x24
SETMODESTRUCT = 0x22  #Unsupported by mfgr.
GETVERSION = 0x23
GETGPIOCAPS = 0x30
GETGPIOCFG = 0x31
SETGPIOCFG = 0x32
GETGPIO = 0x33
SETGPIO = 0x34
REFRESHGPIO = 0x35
DOTXRAW = 0x36
DOTXSTRUCT = 0x37
GETCONFIGURATION = 0x38
kSleepBetweenComm = 0.011
TIMEOUT_DEFAULT = 10

def _openPort():
    global conn
    port = "/dev/tty.usbserial-0000103D"
    conn = serial.Serial(port, 312500, rtscts=True, timeout=1, writeTimeout=1)
    if conn.isOpen() == True:
        print (u"\nConnected to " + conn.name)
        print (u"\nUSB-UIRT\n")
    else:
        conn.open()

def byte2Hex(byteStr):
    return ''.join( [ "0x%02X " % ord( x ) for x in byteStr ] ).strip()

def _calcChecksum(*hexList):
    #return 0x100 - (sum(hexList) & 0xff)
    return ((0x100 - (sum(hexList) & 0xff)) & 0xff)

def _printCommand(prefix, cmd):
    if type(cmd) is tuple: cmd=(chr(x) for x in cmd)
    if DEBUG: print (u"%s: " % prefix + ''.join(["0x%02x " % ord(x) for x in cmd]))


def _sendCommand(*cmd):
    checksum = chr(_calcChecksum(*cmd))
    chrCmd = ''.join(chr(c) for c in cmd) + checksum
    _printCommand("SENDING", chrCmd)
    conn.write(chrCmd)
    #time.sleep(kSleepBetweenComm)


def _readCommand(n):
    ttl = TIMEOUT_DEFAULT
    while ttl > 0:
        data = conn.read(n)
        if data:
            _printCommand("RECEIVED", data)
            return data
        else:
            ttl -= 1
    if ttl == 0:
        print (u"Couldn't communicate with USB-UIRT device after " + TIMEOUT_DEFAULT + " trys. \n")

def _interpretResponse(r, msg):
    if len(r) == 1:
        if ord(r)== TRANSMITTING: print (u"Transmitting")
        elif ord(r) == CMDOK: print (u"Command OK")
        elif ord(r) == CSERROR: print (u"Checksum Error")
        elif ord(r) == TOERROR: print (u"Timeout Error")
        elif ord(r) == CMDERROR: print (u"Command Error")
        else: print (u"%s" % msg)
    else: return None

def _sendGetFirmwareInfo():
    conn.flushInput()
    print (u"\nGetting firmware information...")
    _sendCommand(GETVERSION)
    data = _readCommand(8)
    if len(data) == 8:
        fwmin = ord(data[0])
        fwmaj = ord(data[1])
        pcompmin = ord(data[2])
        pcompmaj = ord(data[3])
        fwday = ord(data[4])
        fwmon = ord(data[5])
        fwyear = ord(data[6])
        print (u"Firmware information: \n")
        print (u"\tFirmware Version = %d.%d" % (fwmaj, fwmin))
        print (u"\tProtocol Version = %d.%d" % (pcompmaj, pcompmin))
        print (u"\tFirmware Date (MDY) = %02d/%02d/%02d\n" % (fwmon, fwday, fwyear + 2000))
    else:
        print (u"Error reading version information.")




def _sendGetConfigInfo():
    conn.flushInput()
    print (u"\nGetting configuration...")
    _sendCommand(GETCONFIGURATION, 0x01)
    data = _readCommand(4)
    if len(data) == 4:
        print (u"Configuration: \n")
        print (u"\tLED blink on IR TX: "), "yes" if (ord(data[0]) & 0x01) == 0x01 else "no"
        print (u"\tLED blink on IR RX: "), "yes" if (ord(data[0]) & 0x02) == 0x02 else "no"
    else:
        print (u"Error getting configuration.")


def _sendSetRawMode():
    print (u"\nSetting RAW mode...")
    _sendCommand(SETMODERAW)
    data = _readCommand(1)
    if len(data) == 1:
        if ord(data[0]) == CMDOK:
           print "CMDOK"
        else:
            print (u"Error setting raw mode.")

def _sendSetRaw2Mode():
    print (u"\nSetting RAW2 mode...")
    _sendCommand(SETMODERAW2)
    data = _readCommand(1)
    _interpretResponse(data, "Error setting RAW2 mode.")

#def _compareCodes(first, second):
#    return first[2:] == second[2:]
    
def _calcInterSpace(data):
    i = (data[0] << 8)
    i |= data[1]
    i = i * 500 / 512
    return i
    
def _calcPulse(data):
    offset = 0
    p = data[0] << 8
    p |= data[1]
    c = data[2]  # number of carrier cycles
    if (c & 0x80):
        c = ((c & 0x7F) << 8) | data[3]
        offset = 1
    if (c != 0):
        f = (250000 / p) * (10 * c - 5)
        #print (u"p = %u, c = %u, f = %u" % (p, c, f))
        freqs.append(f)
        #freq_total += f  <- sum it later
        #nof_freq_samples += 1 <- len it later
    # Record the pulse
    pulses.append(p)
    #nof_pulses += 1 <- len it later
    return offset
    
def _calcSpace(data):
    n = 0
    # Time in 400ns units
    s = data[0]
    if (s == 0xFF):
        #done = 2?
        return 1
    s = (s << 8) | data[1]
    if (s > 0x3E80):
        #print (u"s = %X" % s)
        #done = 1
        return 2
    # Record the space
    spaces.append(s)
    #nof_spaces += 1  <-len it later
    return 0
    
def _calcFreq():
    global calc_freq
    if (len(freqs)):
        calc_freq = sum(freqs) / len(freqs)
    else:
        pass
    print (u"calc_freq = %u"% calc_freq);
    return 0
    
def _parseRaw2(data):
    global interSpace, pulses, spaces, freqs
    pulses = []
    spaces = []
    freqs = []
    state = "INTERSPACE"
    n = 0
    while (n != (len(data))):
        if state == "INTERSPACE":
            #print "INTERSPACE"
            interSpace = _calcInterSpace(data[0:2])
            n += 2
            state = "PULSE"
        elif state == "PULSE":
            #print "PULSE"
            offset = _calcPulse(data[n:n+5])
            n += (3 + offset)
            state = "SPACE"
        elif state == "SPACE":
            #print "SPACE"
            ret = _calcSpace(data[n:n+3])
            #if ret != 0: break
            n += 2
            state = "PULSE"
    #print "CALC FREQ"
    _calcFreq()
    state = "INIT"
    return 0
    
def _outputRaw2():
    global txData
    n = 0
    txData = []
    rawCmd = 0x36
    repCnt = 0x04
    v = 2500000 / calc_freq
    if (v >= 0x80):
        print (u"Error: invalid freq byte value = 0x%02x" % v)
    else:
        print (u"freq byte value = %Xh" % v)
    txData.insert(n, rawCmd)  # RAW command
    print "0x%02x: DOTXRAW Extended Command \n" % txData[n]
    n += 1
    txData.insert(n, ((6 + (len(pulses) + len(spaces))) & 0xFF)) # RAW command length
    print "0x%02x: Command Length \n" % ((6 + (len(pulses) + len(spaces))) & 0xFF)
    n += 1
    txData.insert(n, v) # frequency
    print "B0 0x%02x: Frequency \n" % v
    n += 1
    txData.insert(n, repCnt)   # repeat count
    print "B1 0x%02x: Repeat Count \n" % repCnt
    n += 1
    txData.insert(n, (interSpace >> 8))  # interspace high
    print "B2 0x%02x: Interspace High Byte \n" % (interSpace >> 8)
    n += 1
    txData.insert(n, (interSpace & 0xff))   # interspace low
    print "B3 0x%02x: Interspace Low Byte \n" % (interSpace & 0xff)
    n += 1
    txData.insert(n, ((len(pulses) + len(spaces)) & 0xFF))  # RAW Byte Count
    print "B4 0x%02x: RAW Byte Count \n" % ((len(pulses) + len(spaces)) & 0xFF)
    n += 1
   
    _nof_pulses = len(pulses)
    _nof_spaces = len(spaces)
    nof_fudge = 0
    
    while (_nof_pulses or _nof_spaces):
        if (_nof_pulses):
            t = 560 * pulses[len(pulses) - _nof_pulses] / calc_freq
            print (u"pulse %02Xh" % t)
            if (t >= 0x80):
                txData.insert(n, (0x80 | (t >> 8)))
                n += 1
                txData.insert(n, (t & 0xFF))
                n += 1
                nof_fudge += 1
            else:
                txData.insert(n, t)
                n += 1
            _nof_pulses -= 1
        if (_nof_spaces):
            t = 560 * spaces[len(spaces) - _nof_spaces] / calc_freq
            print (u"space %02Xh" % t);
            if (t >= 0x80):
                txData.insert(n, (0x80 | (t >> 8)))
                n += 1
                txData.insert(n, (t & 0xFF))
                n += 1
                nof_fudge += 1
            else:
                txData.insert(n, t)
                n += 1
            _nof_spaces -= 1
    print (u"txData[1] = 0x%02X, txData[6] = 0x%02X, nof_fudge = 0x%02X" % (txData[1], txData[6], nof_fudge))        
    txData[1] += nof_fudge # redo length to take fudge into account
    txData[6] += nof_fudge
    #print ((0x100 - (sum(txData) & 0xff)) & 0xff)
    txData.append((0x100-(sum(txData) & 0xff)) & 0xff)  # checksum
    n += 1
    return n
            
#def _getReceiveData():
#    tries = 6
#    identical = 0
##    code1 = list()
 #   data1 = 0
 #   code2 = list()
 #   data2 = 0
 #   print "\nPress a button on the remote to capture..."
 #   while data1 != chr(0xFF):
 #       conn.flushOutput()
 #       data1 = conn.read(1)
 #       if data1: code1.append(ord(data1))
 #   print code1
 #   print "\nPress the same button on the remote to capture again..."
 #   while tries > 0 and identical == 0:
 #       while data2 != chr(0xFF):
 #           conn.flushOutput()
 #           data2 = conn.read(1)
 #           if data2: code2.append(ord(data2))
 #       print code2
 #       identical = _compareCodes(code1, code2)
 #       print "Identical: ", identical==1
 #       if identical == 1: return code1
 #       if tries > 1 and identical==0:
 #           print "tries left: %d" % tries
 #           tries -= 1
 #           code1 = code2
 #           code2 = []
 #           data2 = 0
 #           print (u"Codes are not identical. Please press the button again...\n")
 #           conn.flush()
 #   if tries == 0: 
 #       print (u"Couldn't get identical codes! Exiting....\n")
 #       return 0
def _compareCodes(first, second):
    return first[2:] == second[2:]
    
def LongestCommonSubstring(S1, S2):
    M = [[0]*(1+len(S2)) for i in xrange(1+len(S1))]
    longest, x_longest = 0, 0
    for x in xrange(1,1+len(S1)):
        for y in xrange(1,1+len(S2)):
            if S1[x-1] == S2[y-1]:
                M[x][y] = M[x-1][y-1] + 1
                if M[x][y]>longest:
                    longest = M[x][y]
                    x_longest  = x
            else:
                M[x][y] = 0
    return S1[x_longest-longest: x_longest]

def _readCode():
    data = 0
    code = []
    while data != chr(0xFF):
        conn.flushOutput()
        data = conn.read(1)
        if data:
            code.append(ord(data))
    return code

def _getReceiveData():
    tries = 6
    comCode = []
    print "\nPress a button on the remote to capture..."
    code1 = _readCode()
    print code1
    print "\nPress the same button on the remote to capture again..."
    while tries > 0:
        code2 = _readCode()
        print code2
        comCode += LongestCommonSubstring(code1, code2)
        #comCode = code1[0:2] + LongestCommonSubstring(code1, code2) + code1[-1:]
            #print comCode
            #return comCode
        #identical = _compareCodes(code1, code2)
        #print "Identical: ", identical
        #if identical:
        #    return code1
        if tries > 1:
            print "tries left: %d" % tries
        tries -= 1
        code1 = code2
        #print "Codes are not identical. Please press the button again...\n"
        conn.flush()
    comCode = code1[0:2] + comCode + code1[-1:]
    print comCode
    return comCode
    #print "Couldn't get identical codes! Exiting....\n"
    #return 0

def _sendTransmitData(data):
    chrCmd = ""
    conn.flushInput()
    print (u"\nReady to transmit...")
    chrCmd = ''.join(chr(c) for c in data)
    conn.write(chrCmd)
    data = _readCommand(1)
    _interpretResponse(data, "Error transmitting.")


_openPort()
_sendGetFirmwareInfo()
_sendGetConfigInfo()
#_sendSetRawMode()
_sendSetRaw2Mode()
code = _getReceiveData()
if (code): _parseRaw2(code)
else: sys.exit()
_outputRaw2()
_sendTransmitData(txData)

#print ' '.join(["0x%02x" % x for x in txData])

print "\nClosing connection..."
conn.close()
print "\nDone."
