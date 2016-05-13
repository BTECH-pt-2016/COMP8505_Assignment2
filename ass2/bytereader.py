import binascii

f = open("100.bmp", "rb")
j = open("good.bmp", "wb")

try:
	data = f.read()
	x = binascii.hexlify(data)
	j.write(binascii.unhexlify(x))
finally:
	f.close()