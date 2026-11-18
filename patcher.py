d = bytearray(open('huion_backup_original.bin','rb').read())
assert d[0x3316:0x3318] == bytes.fromhex('7048'), 'not the expected stock file'
d[0x3316:0x3318] = bytes.fromhex('c0e0')
open('huion_backup_nofilter.bin','wb').write(d)
