import base64
from Crypto.Cipher import AES
from Crypto import Random
import binascii

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]


def encrypt( text, key ):
    text = pad(text)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )
    return binascii.hexlify(base64.b64encode( iv + cipher.encrypt( text ) ))

def decrypt( encText, key ):
    enc = base64.b64decode(binascii.unhexlify(encText))
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))

filename = 'test.txt'
with open(filename) as f:
    content = f.read()
key = "abcabcabcabcabca"# the length has to be multiple of 16
encrypted = encrypt(content, key)
print decrypt(encrypted , key)
