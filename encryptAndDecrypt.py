import base64
from Crypto.Cipher import AES
from Crypto import Random
import binascii
import os
import sys

BS = 16

def encrypt( text, key ):
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    text = pad(text)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )
    return binascii.hexlify(iv + cipher.encrypt( text ) )

def decrypt( encText, key ):
    unpad = lambda s : s[:-ord(s[len(s)-1:])]
    enc = binascii.unhexlify(encText)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))

if len(sys.argv) != 2:
    print "please put file path"
    print "Usage: python encryptAndDecrypt.py <filepath>"
    sys.exit()
else:
    filename = sys.argv[1]

with open(filename) as f:
    content = f.read()
key = "abcabcabcabcabca"# the length has to be multiple of 16
encrypted = encrypt(content+"^"+filename.split("/")[-1], key)

decrypted = decrypt(encrypted , key)
filename2 = decrypted.split("^")[-1]
writepath = 'decrypted/'+filename2
content2 =  decrypted[:-len(filename2)+1]

with open(writepath, 'w') as f:
    f.write(content2)
