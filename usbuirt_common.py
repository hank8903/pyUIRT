#!/usr/bin/env python


# Units
UNIT = 50  # 50u
# 51.2uS
V5IS_MULT = 512
V5IS_DIV = 10
# 400nS
V5PS_MULT = 4
V5PS_DIV = 10

# Commands
SETMODEUIR = 0x20
SETMODERAW = 0x21
SETMODEDESTRUC = 0x22
GETVERSION = 0x23
SETMODEV5RAW = 0x24
GETGPIOCAPS = 0x30
GETGPIOCFG = 0x31
SETGPIOCFG = 0x32
GETGPIO = 0x33
SETGPIO = 0x34
REFRESHGPIO = 0x35
DOTXRAW = 0x36
DOTXSTRUCT = 0x37

# Responses
TRANSMITTING = 0x20
CMDOK = 0x21
CSERROR = 0x80
TOERROR = 0x81
CMDERROR = 0x82

# Actions

# Ports

# Frequencies
FREQ_40 = 0x00
FREQ_38 = 0x40
FREQ_36 = 0xC0

# Setmode
MODE_UIR = 0x00
MODE_RAW = 0x01
MODE_STRUC = 0x02
MODE_V5RAW = 0x03
MODE_MASK = 0x03

# Extended Flags

global fd, flags, fw_version, rd_rp, rd_wp, rd_buf
global carrier_freq, cf_total, cf_count, pre_delay, pre_time, new_signal

def hexdump(buf, len):
    i = 0
    str = []
    pos = 0

    for (i = 0; i < len; i+=1):
        if (pos + 3 >= sizeof(str)):
            break
        if (!(i % 8)):
            str[pos] = ' '
            pos += 1

        print str + pos + "%02x" % buf[i]

        pos += 3

    print(u"%s" % str)


#def mywaitfordata(dev, usec):

def checksum(data, len):
    check = 0
    i = 0
    
    for (i = 0; i < len; i += 1)
        check = check - data[i]

    return check & 0xff

#def command_ext(dev, in, out):

def command(dev, buf, len):
    in = []
    out = []
  
    #memcpy(in + 1, buf, len+1)
    in[0] = len
    out[0] = 1

    if (command_ext(dev, in, out, 0) < 0):
        return -1

    return out[1] < CSERROR

#def calc_bits_length(buf):

#def calc_bits_usb_length(buf):
        
def calc_raw_usb_length(buf):
    i = 0
    tot = 0
    bISDly = UNIT * (buf[3] + 256 * buf[2])
    bcnt = buf[4]
    for (i=0; i<bcnt; i+=1):
        tot += buf[i+5]
    tot *= ((buf[0] & 0x7f) * 4) / 10

    return (repeat + 1) * (bISDly + tot)

#def calc_struct1_length(buf):

#def calc_struct1_usb_length(buf):



#+uirt2usb_t *uirt2usb_init(int fd);
def ini(fd):
    #dev = conn
    version = 0

    if(dev == NULL):
        print(u"raw: out of memory")
        return NULL

    #memset(dev, 0, sizeof(uirt2usb_t))

    new_signal = 1
    flags = MODE_UIRT
    fd = _fd

    rd_wp = rd_rp = 0
    #buf = malloc....

    if(getversion(dev, version) < 0):
        free(buf)
        fre(dev)
        return NULL

    fw_version = version
    if (version < 0x0104):
        print(u"raw: Old UIRT hardware")
    else:
        print(u"raw: UIRT version %04x ok" % version)

    return dev


#+int uirt2usb_uninit(uirt2usb_t *dev);
def uninit(dev):
    fre(bif)
    free(dev)
    return 0


#+int uirt2usb_fw_version(uirt2usb_t *dev);
def fw_version(dev):
    return fw_version

#+int uirt2usb_getcarrier_freq(uirt2usb_t *dev);
def getcarrier_freq(dev):
    return carrier_freq

def getmode(dev):
    return (flags & MODE_MASK)


#+int uirt2usb_getfd(uirt2usb_t *dev);

def setmode(dev, mode):
    buf = []
    cmd = 0

    if getmode(dev) == mode):
        print (u"setmode: already in requensted mode")
        return 0

    if mode == MODE_UIR:
         cmd = SETMODEUIR
    elif mode == MODERAW:
        cmd = SETMODERAW
    elif mode = MODE_V5RAW::
        if (fw_version > 0x503):
            cmd = SETMODEV5RAW
        else:
            cmd = SETMODERAW
    elif mode == MODE_STRUC:
        cmd = SETMODESTRUC
    else:
        print (u"raw: bad mode")
        return -1

    buf[0] = cmd
    print(u"setmode: cmd 1 %02x" % cmd)
    if (command(dev, buf, 0) < 0):
        print(u"raw: setmode failed")
        return -1

    print (u"setmode: cmd 2 %02x" % cmd)
    flags = (flags & MODE_MASK) | mode
    return 0


#+int uirt2usb_setmodeuir(uirt2usb_t *dev);
def setmodeuir(dev):
    return setmode(dev, MODE_UIR)

#+int urt2usb_setmodelearn(uirt2usb_t *dev);
def setmodelearn(dev):
    return setmode(dev, MODE_V5RAW)

#+int urt2usb_setmoderaw(uirt2usb_t *dev);
def setmoderaw(dev):
    return setmode(dev, MODE_RAW)

#+int urt2usb_setmodestruc(uirt2usb_t *dev);
def setmodestruc(dev):
    return setmode(dev, MODE_STRUC)

#+int urt2usb_getversion(uirt2usb_t *dev, int *version);
def getversion(dev, version):
    out = []
    in = []

    in[0] = 0
    in[1] = GETVERSION
    out[0] = 3

    if (command_ext(dev, in , out, 8) < 0 ):
        return -1

    version = out[1] + (out[2] << 8)
    return 0

#+int urt2usb_getgpiocaps(uirt2usb_t *dev, int *slots, byte_t masks[4]);
def getgpiocaps(dev, slots, masks[4]):
    in = []
    out = []
   
    in[0] = 1
    in[1] = GETGPIOCAPS
    in[2] = 1

    out[0] = 6

    if (command_ext(dev, in, out, 0) < 0):
        return -1

    slots = out[1]
    #memcpy(masks, out +2, 4)
    retrn 0



#+int urt2usb_getgpiocfg(uirt2usb_t *dev, int slot, uirt2usb_code_t code,
#		     int *action, int *duration);


#int uirt2usb_setgpio(uirt2usb_t *dev, int action, int duration);
def setgpio(dev, action, duration):
    buf = []
    buf[0] = SETGPIO
    buf[1] = 3
    buf[2] = action
    buf[3] = duration / 5

    return command(dev, buf, 3)

#int uirt2usb_read_uir(uirt2usb_t *dev, byte_t *buf, int length);


#lirc_t uirt2usb_read_raw(uirt2usb_t *dev, lirc_t timeout);
def read_raw(dev, timeout):
    data = 0
    pulse = 0
    
    if (getmode(dev) == MODE_V5RAW):
        while (1):
            res = 0
            b = []
            
            if (rd_wp <= rd_rp):
                if (!waitfordata(timeout)):
                    print(u"read_raw_e1 timeout")
                    rd_wp = rd_rp = 0
                    return 0
            res = buf_rd(dev, b[0], timeout)
            if (res < 0):
                print(u"read_raw_e res: %d" % res)
                return 0
                
            print (u"read_raw_e %02x" % b[0])
            if (b[0] == 0xff):
				new_signal = 1
				if (cf_count)
					carrier_freq = cf_total
						/ cf_count;
				cf_total = cf_count
					= rd_wp = rd_rp = 0;
				continue;
	

			if (new_signal):
				print(u"e dev->new_signal")
				res = buf_rd(dev, b[1], timeout)
				if (res < 0) {
					print (u"read_raw_e1 res: %d" % res)
					return 0
				
				print(u"read_raw_e1 %02x" % b[1])
				data = (((b[0] << 8) + b[1]) * V5IS_MULT) / V5IS_DIV
				pulse = 1
				new_signal = 0
			else:
			    if (pulse):
					i = 0
					j = 0

					for (i = 1; i < 3; i+=1):
						res = buf_rd(dev, b[i], timeout)
						if (res < 0):
							print (u"read_raw_e2 res: %d" % res)
							return 0
						
					
					if (b[2] >= 0x80):
						res = buf_rd(dev, b[3], timeout)
						if (res < 0):
							print(u"read_raw_e3 res: %d" % res)
							return 0
						
						b[2] &= 0x7f
					else:
						b[3] = b[2]
						b[2] = 0
					
					print(u"read_raw_e pulse %02x%02x%02x%02x" % (b[0],b[1],b[2],b[3]))
					i = (((b[0] << 8) + b[1]) * V5PS_MULT) / V5PS_DIV
					j = (((b[2] << 8) + b[3]) << 1) - 1
					print(u"read_raw_e i j %d %d" % (i, j))
					data = i | PULSE_BIT
					i *= 2
					cf_total += (1000000 * j) / i
					cf_count+=1
					print(u"read_raw carrier %d" % ((1000000 * j) / i))
				else:
					res = buf_rd(dev, b[1], timeout)
					if (res < 0):
						print(u"read_raw_e4 res: %d" & res)
						return 0
					
					print(u"read_raw_e space %02x%02x" % (b[0],b[1]))
					data = (((b[0] << 8) + b[1]) * V5PS_MULT) / V5PS_DIV
				
				pulse = !pulse
			
		return data
		
	elif (getmode(dev) == MODE_RAW):
		while (1):
			res = 0
			b = 0

			if (rd_wp <= rd_rp):
				if (!waitfordata(timeout)):
					print(u"read_raw timeout")
					rd_wp = rd_rp = 0
					return 0
				
			
			res = buf_rd(dev, b, timeout)
			if (res < 0):
				print(u"read_raw res: %d" % res)
				return 0
			
			print(u"read_raw %02x" % b)
			if (!b):
				b+=1
			if (b == 0xff):
				new_signal = 1
				rd_wp = rd_rp = 0
				continue
			

			if (dev->new_signal):
				c = 0

				print (u"new_signal")
				res = buf_rd(dev, c, timeout)
				if (res < 0):
					print(u"read_raw_b res: %d" % res)
					return 0
				
				print(u"read_raw_b %02x" % c)
				data = UNIT * ((b << 8) + c)
				pulse = 1
				new_signal = 0
			else:
				data = UNIT * b
				if (pulse):
					data = data | PULSE_BIT
				
				pulse = !pulse
			
		return data
		
	else:
		print(u"raw: Not in RAW mode")
		return -1
	


#int uirt2usb_send_raw(uirt2usb_t *dev, byte_t *buf, int length);
def send_raw(dev, buf, length):
    tmp = []
    res = 0
    delay = 0
    
    tmp[0] = DOTXRAW
    tmp[1] = length + 1
    #memcpy(tmp + 2, buf, length)
    
    res = command(dev, tmp, length + 1)
    print (u"send_raw: len %d res %d" % (length, res)
    delay = cal_raw_usb_length(buf)
    gettimeofday(pre_time, NULL)
    pre_delay.tv_sec = delay / 1000000
    pre_delay.tv_usec = delay % 1000000
    
    print (u"pre_delay %lu &lu" % (pre_delay.tv_sec, pre_delay.tv_usec)
    return res
    

#int uirt2usb_send_struct1(uirt2usb_t *dev, remstruct1_t *buf);
#int uirt2usb_send_struct1usb(uirt2usb_t *dev, remstruct1_usb_t *buf);

def calc_freq(freq):
    if (freq > 39000):
        return FREQ_40
    elif (freq > 37000):
        return FREQ_38
    else:
        return FREQ_36
