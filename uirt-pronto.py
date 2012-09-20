#!/usr/bin/env python

import serial

#pronto = raw_input('Pronto: \n')

pronto = "0000 006f 0000 0125 000f 0030 000f 0030 000f 0030 002f 0010 002f 0010 002f 0030 000f 0010 002f 0010 002f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0010 002f 0010 002f 0030 002f 0010 000f 0010 002f 0030 002f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0010 000f 0010 002f 0030 002f 0010 002f 0010 000f 0030 002f 0030 002f 0030 000f 0030 000f 0030 000f 0030 000f 0010 000f 0010 000f 0030 002f 0010 002f 0010 002f 0030 000f 0030 002f 0030 002f 0030 000f 0030 000f 0030 000f 0010 000f 0010 000f 0030 000f 0010 002f 0010 002f 0030 002f 0030 000f 0030 002f 0030 002f 0030 000f 0030 000f 0010 000f 0010 000f 0030 000f 0010 000f 0010 002f 0030 002f 0030 002f 0030 000f 0030 002f 0030 002f 0030 000f 0010 000f 0010 000f 0030 000f 0010 000f 0010 000f 0030 002f 0030 002f 0030 002f 0030 000f 0030 002f 0030 002f 0010 000f 0010 000f 0030 000f 0010 000f 0010 000f 0030 000f 0030 002f 0030 002f 0030 002f 0030 000f 0030 002f 0010 002f 0010 000f 0030 000f 0010 000f 0010 000f 0030 000f 0030 000f 0030 002f 0030 002f 0030 002f 0030 000f 0010 002f 0010 002f 0030 000f 0010 000f 0010 000f 0030 000f 0030 000f 0030 000f 0030 002f 0030 002f 0030 002f 0010 000f 0010 002f 0030 002f 0010 000f 0010 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 002f 0030 002f 0010 002f 0010 000f 0030 002f 0010 002f 0010 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 002f 0010 002f 0010 002f 0030 000f 0010 002f 0010 002f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0010 002f 0010 002f 0030 002f 0010 000f 0010 002f 0030 002f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0010 000f 0010 002f 0030 002f 0010 002f 0010 000f 0030 002f 0030 002f 0030 000f 0030 000f 0030 000f 0030 000f 0010 000f 0010 000f 0030 002f 0010 002f 0010 002f 0030 000f 0030 002f 0030 002f 0030 000f 0030 000f 0030 000f 0010 000f 0010 000f 0030 000f 0010 002f 0010 002f 0030 002f 0030 000f 0030 002f 0030 002f 0030 000f 0030 000f 0010 000f 0010 000f 0030 000f 0010 000f 0010 002f 0030 002f 0030 002f 0030 000f 0030 002f 0030 002f 0030 000f 0010 000f 0010 000f 0030 000f 0010 000f 0010 000f 0030 002f 0030 002f 0030 002f 0030 000f 0030 002f 0030 002f 0010 000f 0010 000f 0030 000f 0010 000f 0010 000f 0030 000f 0030 002f 0030 002f 0030 002f 0030 000f 0030 002f 0010 002f 0010 000f 0030 000f 0010 000f 0010 000f 0030 000f 0030 000f 0030 002f 0030 002f 0030 002f 0030 000f 0010 002f 0010 002f 0030 000f 0010 000f 0010 000f 0030 000f 0030 000f 0030 000f 0030 002f 0030 002f 0030 002f 0010 000f 0010 002f 0030 002f 0010 000f 0010 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 002f 0030 002f 0010 002f 0010 000f 0030 002f 0010 002f 0010 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 000f 0030 002f 0010 002f 002f 000f 002f 002f 000f 000f 000f 000f 000f 000f 002f 002f 002f 000f 002f 002f 000f 000f 000f 000f 000f 000f 002f 002f 0175"

#pronto = "0000 0069 0000 0020 000b 0047 000b 001f 000b 0047 000b 0047 000b 001f 000b 001f 000b 0047 000b 0047 000b 001f 000b 0047 000b 001f 000b 0047 000b 001f 000b 0047 000b 001f 000b 069a 000b 0047 000b 001f 000b 0047 000b 0047 000b 001f 000b 0047 000b 001f 000b 001f 000b 0047 000b 001f 000b 0047 000b 001f 000b 0047 000b 001f 000b 0047 000b 069a"

#pronto = "0000 0067 0000 0015 0060 0018 0018 0018 0030 0018 0030 0018 0030 0018 0018 0018 0030 0018 0018 0018 0018 0018 0030 0018 0018 0018 0030 0018 0030 0018 0030 0018 0018 0018 0018 0018 0030 0018 0018 0018 0018 0018 0030 0018 0018 03f6"

def rpStr_list(data):
    l = data.replace(' ','')
    return [int(l[i:i+2],16) for i in xrange(0, len(l), 2)]

def rp_init(data):
    global pulse, space, nof_spaces, nof_pulses
    global txData, freq, rptCnt, interSpace
    txData = []
    pulse = []
    space = []
    nof_spaces = 0
    nof_pulses = 0
    interSpace = 0
    rptCnt = 4
    n = 0
    # Skip Header (Assume is 0000)
    n += 2
    
    # frequency
    f = data[n] << 8
    n += 1
    f |= data[n]
    n += 1
    # actual calculation is 4145146.44802 / f
    freq = 4145146 / f

    # Skipping over difference between burst sequences for now
    n += 4

    return n

def rp_pulse(data):
    global pulse, nof_pulses
    n = 0
    
    # time in carrier cycles
    p = data[n] << 8
    n += 1
    p |= data[n]
    n += 1

    #record the pulse
    pulse.insert(nof_pulses, p)
    nof_pulses += 1

    print (u"pulse = 0x%02x" % p)

    return n

def rp_space(data):
    global space, nof_spaces
    n = 0

    # time in carrier cycles
    s = data[n] << 8
    n += 1
    s |= data[n]
    n += 1

    # record the space
    space.insert(nof_spaces, s)
    nof_spaces += 1

    print (u"space = 0x%02x" % s)

    return n

def rp_parse(data):
    n = 0
    state = "INIT"

    while (n < len(data)):
        if state == "INIT":
            i = rp_init(data[n:])
            n += i
            state = "PULSE"
        elif state == "PULSE":
            i = rp_pulse(data[n:])
            n += i
            state = "SPACE"
        elif state == "SPACE":
            i = rp_space(data[n:])
            n += i
            state = "PULSE"
        else:
            pass      
    # n += fn(ctx, d[n])

    return 0

def rp_output(data):
    global nof_pulses, nof_spaces, nof_fudge, rptCnt

    n = 0

    print (u"Calculated frequency %u\n" % freq)

    v = 2500000 / freq
    if (v >= 0x80):
        print (u"Invalid freq byte value = %Xh\n" % v)
    else:
        print (u"Freq byte value = %Xh\n" % v)

    txData.insert(n, 0x36)  # RAW Command
    n += 1
    txData.insert(n, (6 + ((nof_pulses + nof_spaces) & 0xff)))  # RAW Cmd Len
    n += 1
    txData.insert(n, v)  # Frequency
    n += 1
    txData.insert(n, rptCnt)   # Repeat Count
    n += 1
    txData.insert(n, (interSpace >> 8))  # Interspace High
    n += 1
    txData.insert(n, (interSpace & 0xff))  # Interspace Low
    n += 1
    txData.insert(n, ((nof_pulses + nof_spaces) & 0xff))
    n += 1

    _nof_pulses = nof_pulses
    _nof_spaces = nof_spaces
    nof_fudge = 0

    while (_nof_pulses or _nof_spaces):
        if (_nof_pulses):
            t = pulse[nof_pulses - _nof_pulses]
            if (t >= 0x80):
                txData.insert(n, (0x80 | (t >> 8)))
                n += 1
                txData.insert(n, (t & 0xff))
                n += 1
                nof_fudge += 1
            else:
                txData.insert(n, t)
                n += 1
            
            _nof_pulses -= 1

        if (_nof_spaces):
            t = space[nof_spaces - _nof_spaces]
            if (t >= 0x80):
                txData.insert(n, (0x80 | (t >> 8)))
                n += 1
                txData.insert(n, (t & 0xff))
                n += 1
                nof_fudge += 1
            else:
                txData.insert(n, t)
                n += 1
            
            _nof_spaces -= 1              
   
    print (u"txData[1] = 0x%02x, txData[6] = 0x%02x, nof_fudge = 0x%02x\n" % (txData[1], txData[6], nof_fudge))
    txData[1] += nof_fudge  # redo the length to take fudge into account
    txData[6] += nof_fudge
    txData.append((0x100 - (sum(txData) & 0xff) & 0xff ))
    print ''.join([("%02x" % (0xff & x)) for x in txData])
    return n




plist = rpStr_list(pronto)
print plist
rp_parse(plist)
rp_output(plist)


port = "/dev/tty.usbserial-0000103D"
conn = serial.Serial(port, 312500, rtscts=True, timeout=1)


print txData

chrCmd = ''.join(chr(c) for c in txData)
conn.setDTR(False)
conn.write(chrCmd)
conn.setDTR(True)
data = conn.readline()

print "\n\nResponse:"
print ''.join( [ "0x%02X " % ord( x ) for x in data ] )

conn.close()
