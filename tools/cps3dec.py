# CPS3 decrypt (algorithm from MAME cps3.cpp, BSD-3). usage: cps3dec.py romdir outdir
import sys, os, struct
K1, K2 = 0x23323ee3, 0x03021972
def rol(v, n): return ((v << n) | (v >> (16 - n))) & 0xffff
def rotxor(v, x):
    r = (v + rol(v, 2)) & 0xffff
    return rol(r, 4) ^ (r & (v ^ x))
def mask(a):
    a ^= K1
    v = (a & 0xffff) ^ 0xffff
    v = rotxor(v, K2 & 0xffff)
    v ^= (a >> 16) ^ 0xffff
    v = rotxor(v, K2 >> 16)
    v ^= (a & 0xffff) ^ (K2 & 0xffff)
    return v | (v << 16)
def dec(data, base):
    n = len(data) // 4
    w = struct.unpack('>%dI' % n, data)
    return struct.pack('>%dI' % n, *[x ^ mask(base + i * 4) for i, x in enumerate(w)])
src, out = sys.argv[1], sys.argv[2]
bios = open(os.path.join(src, 'jojoba_euro_nocd.29f400.u2'), 'rb').read()
open(os.path.join(out, 'bios_dec.bin'), 'wb').write(dec(bios, 0))
for s, base in ((1, 0x06000000), (2, 0x06800000)):
    ch = [open(os.path.join(src, 'jojoba-simm%d.%d' % (s, c)), 'rb').read() for c in range(4)]
    il = bytes(b for q in zip(*ch) for b in q)
    open(os.path.join(out, 'simm%d_raw.bin' % s), 'wb').write(il)
    open(os.path.join(out, 'simm%d_dec.bin' % s), 'wb').write(dec(il, base))
