#!/usr/bin/env python

import serial
import time
import os

class dataState:
    INIT=1
    INTERSPACE=2
    PULSE=3
    SPACE=4
	
UIRT_CMD_O_LENGTH = 1
UIRT_CMD_TX_RAW_O_LENGTH = 6


rcvd = [131, 82, 4, 3, 16, 12, 150, 4, 3, 16, 12, 148, 4, 3, 16, 12, 16, 12, 145, 4, 3, 16, 12, 145, 4, 10, 16, 12, 145, 12, 83, 48, 70, 187, 12, 83, 48, 4, 66, 12, 85, 48, 4, 68, 4, 8, 16, 12, 145, 12, 83, 48, 4, 70, 12, 83, 48, 4, 68, 4, 8, 16, 12, 145, 4, 8, 16, 12, 145, 4, 3, 16, 12, 150, 4, 3, 16, 12, 148, 4, 4, 8, 16, 12, 145, 4, 3, 16, 12, 150, 12, 83, 48, 70, 185, 12, 83, 48, 4, 68, 12, 83, 48, 4, 69, 4, 8, 16, 12, 143, 12, 88, 48, 4, 12, 83, 48, 70, 185, 12, 83, 48, 4, 71, 12, 83, 48, 4, 66, 4, 8, 16, 12, 148, 12, 83, 48, 4, 68, 12, 83, 48, 4, 4, 3, 16, 12, 148, 12, 83, 48, 4, 73, 12, 78, 48, 4, 71, 4, 3, 16, 12, 153, 4, 3, 16, 12, 148, 4, 3, 16, 12, 150, 4, 3, 16, 12, 145, 4, 3, 16, 12, 150, 4, 3, 16, 12, 148, 12, 83, 48, 70, 189, 12, 83, 48, 4, 68, 12, 83, 48, 4, 69, 4, 3, 16, 12, 150, 12, 83, 48, 4, 66, 12, 83, 48, 4, 73, 4, 3, 16, 12, 4, 8, 16, 12, 145, 4, 3, 16, 12, 150, 4, 3, 16, 12, 148, 4, 3, 16, 12, 147, 4, 8, 16, 12, 147, 12, 83, 48, 255]


def _initTxRaw():
    global pulse, space, nof_spaces, nof_pulses
    global freq_total
    global nof_freq_samples
    global txData, repCnt, prontoData
    pulse = []
    space = []
    nof_spaces = 0
    nof_pulses = 0
    freq_total = 0
    nof_freq_samples = 0
    txData = []
    prontoData = []
    repCnt = 0x04
    return 0
    
def _calcInterspace(data):
    global interSpace
    # if (dataLen < 2) return -dataLen  ??
    n = 0
    i = (data[n] << 8)
    n += 1
    i |= data[n]
    n += 1
    i = i * 500 / 512
    interSpace = i
    return n
    
def _calcPulse(data):
    global freq_total, nof_freq_samples, nof_pulses, pulse
    n = 0
    #if (dataLen < 3) return -len ??
    p = data[n] << 8
    n += 1
    p |= data[n]
    n += 1
    c = data[n]  # number of carrier cycles
    n += 1
    if (c & 0x80):
        #if (len < 4) return -len 
        c = ((c & 0x7F) << 8) | data[n]
        n += 1
    if (c != 0):
        f = (250000 / p) * (10 * c - 5)
        print (u"p = %u, c = %u, f = %u" % (p, c, f))
        if f > 37000:    
            freq_total += f
            nof_freq_samples += 1
    # Record the pulse
    pulse.insert(nof_pulses,p)
    nof_pulses += 1
    return n
    
def _calcSpace(data):
    global nof_spaces, space
    n = 0
    #if (len < 1) return -len
    # Time in 400ns units
    s = data[n]
    n += 1
    if (s == 0xFF):
        #done = 2?
        return n
    #if (len < 2) return -len
    s = (s << 8) | data[n]
    n += 1
    if (s > 0x3E80):
        print (u"s = %X" % s)
        #done = 1
        return n
    # Record the space
    space.insert(nof_spaces,s)
    nof_spaces += 1
    return n
    
    
def _calcFinal(data):
    global calc_freq
    if (nof_freq_samples):
        #calc_freq = 38
        calc_freq = freq_total / nof_freq_samples
    else:
        calc_freq = 1 # something that won't crash
    print (u"calc_freq = %u"% calc_freq);
    return 0

def _parseRaw2(data):
    global nof_spaces, nof_pulses, pulse, space, nof_freq_samples
    m = n = 0
    nextState = dataState.INIT
    while (n < (len(data) / 3)):
        #print n
        if (n == len(data) - 1): break
        elif nextState == dataState.INIT:
            #print "INITIALIZE"
            _initTxRaw()
            nextState = dataState.INTERSPACE
        elif nextState == dataState.INTERSPACE:
            #print "INTERSPACE"
            i = _calcInterspace(rcvd[n:])
            n += i
            nextState = dataState.PULSE
        elif nextState == dataState.PULSE:
            #print "PULSE"
            i = _calcPulse(rcvd[n:])
            n += i
            nextState = dataState.SPACE
        elif nextState == dataState.SPACE:
            #print "SPACE"
            i = _calcSpace(rcvd[n:])
            n += i
            nextState = dataState.PULSE
        #n += m
    _calcFinal(rcvd[n:])
    nextState = dataState.INIT
    return 0

def _outputRaw2(data):
    global nof_pulses, nof_spaces
    n = 0
    v = 2500000 / calc_freq
    if (v >= 0x80):
        print (u"Error: invalid freq byte value = 0x%02x" % v)
    else:
        print (u"freq byte value = %Xh" % v)
    txData.insert(n, 0x36)  # RAW command
    print "0x%02x: DOTXRAW Extended Command \n" % 0x36
    n += 1
    txData.insert(n, ((6 + (nof_pulses + nof_spaces)) & 0xFF)) # RAW command length
    print "0x%02x: Command Length \n" % ((6 + (nof_pulses + nof_spaces)) & 0xFF)
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
    txData.insert(n, ((nof_pulses + nof_spaces) & 0xFF))  # RAW Byte Count
    print "B4 0x%02x: RAW Byte Count \n" % ((nof_pulses + nof_spaces) & 0xFF)
    n += 1
   
    _nof_pulses = nof_pulses
    _nof_spaces = nof_spaces
    nof_fudge = 0
    
    while (_nof_pulses or _nof_spaces):
        if (_nof_pulses):
            t = 560 * pulse[nof_pulses - _nof_pulses] / calc_freq
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
            t = 560 * space[nof_spaces - _nof_spaces] / calc_freq
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
    print (u"txData[1] = %02X, txData[6] = %02X, nof_fudge = %02X" % (txData[UIRT_CMD_O_LENGTH], txData[UIRT_CMD_TX_RAW_O_LENGTH], nof_fudge))        
    txData[UIRT_CMD_O_LENGTH] += nof_fudge # redo length to take fudge into account
    txData[UIRT_CMD_TX_RAW_O_LENGTH] += nof_fudge
    print ((0x100 - (sum(txData) & 0xff)) & 0xff)
    txData.append((0x100-(sum(txData) & 0xff)) & 0xff)  # checksum
    n += 1
    return n
    
def _outputPronto(data):
    n = 0
    prontoData.insert(n, 0)
    n += 1
    prontoData.insert(n, 0)  # learned command
    n += 1
    prontoData.insert(n, 0)
    n += 1
    prontoData.insert(n, (4145146 / calc_freq)) # frequency
    n += 1
    prontoData.insert(n, 0)
    n += 1
    prontoData.insert(n, 0)  # once burst-pair count
    n += 1
    prontoData.insert(n, (nof_pulses >> 8))
    n += 1
    prontoData.insert(n, (nof_pulses & 0xff))  # repeat burst-pair count
    n += 1
    _nof_pulses = nof_pulses
    _nof_spaces = nof_spaces
    while (_nof_pulses or _nof_spaces):
        if (_nof_pulses):
            t = 560 * pulse[nof_pulses - _nof_pulses] / calc_freq
            prontoData.insert(n, (t >> 8))
            n += 1
            prontoData.insert(n, (t & 0xff))
            n += 1
            _nof_pulses -= 1
        if (_nof_spaces):
            t = 560 * space[nof_spaces - _nof_spaces] / calc_freq
            prontoData.insert(n, (t >> 8))
            n += 1
            prontoData.insert(n, (t & 0xff))
            n += 1
            _nof_spaces -= 1
    # Add 10ms as the trailer ( the USB-UIRT end of code gap definition)
    t = calc_freq / 100
    prontoData.insert(n, (t >> 8))
    n += 1
    prontoData.insert(n, (t & 0xff))
    n += 1
    
    return n
                
_parseRaw2(rcvd)
_outputRaw2(rcvd)
#_outputPronto(rcvd)
#print ' '.join([("%02x" % i)+("%02x" % j) for i,j in zip(prontoData[::2],prontoData[1::2])])

port = "/dev/tty.usbserial-0000103D"
conn = serial.Serial(port, 312500, rtscts=True, timeout=1)



print txData
print ' '.join(hex(c) for c in rcvd)
chrCmd = ''.join(chr(c) for c in txData)
conn.setDTR(False)
conn.write(chrCmd)
conn.setDTR(True)
data = conn.readline()

print "\n\nResponse:"
print ''.join( [ "0x%02X " % ord( x ) for x in data ] )

conn.close()
