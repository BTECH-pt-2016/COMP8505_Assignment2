import base64
from Crypto.Cipher import AES
from Crypto import Random
import binascii

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def int2base(a, base, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    baseit = lambda a=a, b=base: (not a) and numerals[0]  or baseit(a-a%b,b*base)+numerals[a%b%(base-1) or (a%b) and (base-1)]
    return baseit()

def encrypt( text, key ):
    key = pad(key)
    text = pad(text)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )
    return binascii.hexlify(iv + cipher.encrypt( text ) )

def decrypt( encText, key ):
    key = pad(key)
    enc = binascii.unhexlify(encText)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))
