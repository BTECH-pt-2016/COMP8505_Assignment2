from PIL import Image
from encryptAndDecrypt import *


# takes the current R or G or B Color as the first argument (0 - 255)
# takes the request remainder you would like to achieve. so in base 3 it would be 0, 1, or 2
# takes the Base you're trying to calculate in our implementation is in base 3
def colorChange(currentColor, requestedVal, baseN):
    currentVal = currentColor % baseN
    distanceToNext = -1

    # color is already correct
    if currentVal == requestedVal:
        return currentColor

    # the current color is 0 (not allowed to go below)
	# return the requested value as it would be the closest color
    if currentColor == 0:
        if requestedVal > 0:
            return requestedVal

	#this calculates the distance the next greater number to achieve the requested value
    if currentVal < requestedVal:
        distanceToNext = requestedVal - currentVal
    else:
        distanceToNext = baseN - currentVal + requestedVal

	# this calculate the distance to the requested value below the current color
    distanceToPrev = currentVal - requestedVal

	# basic checks to make sure we select the least distance to the requested value
	# as well as not to exceed 255 or preceed 0
    if distanceToNext < distanceToPrev:
        if (currentColor + distanceToNext) <= 255:
            return currentColor + distanceToNext
        else:
            return currentColor - distanceToPrev
    else:
        if (currentColor - distanceToPrev) >= 0:
            return currentColor - distanceToPrev
        else:
            return currentColor + distanceToNext

def stegoImage(myImage, encryptedString):
    max = len(encryptedString)
    indexForString = 0
    # i is every pixel horizontally
    for i in range(myImage.size[0]):
	     # j is every pixel vertically
        for j in range(myImage.size[1]):
            # https://pillow.readthedocs.io/en/3.2.x/reference/Image.html#PIL.Image.Image.getpixel
            pixel = myImage.getpixel((i,j))
            newRGB = [0,0,0]

            # if it is the end of the file
            if(max <= indexForString):
                #put 222
                for c in range(2,-1,-1):
                    newRGB[c] = colorChange(pixel[c], 2, 3)
                myImage.putpixel((i,j),tuple(newRGB))
                return
            # get hex value and get base3
            base3NumStr = str(int(int2base(int(encryptedString[indexForString],16),3)))
            # add leading 0
            base3NumStr = "{:0>3}".format(base3NumStr)
		    # this is a for loop that loops through the colors R G and B
            # going backwords 2,1,0
            for c in range(2,-1,-1):
			    # below im requesting the nearest color to achieve "2" in base 3.
			    # NOTE: colorChange returns the colorValue which will produce the value "2" once it goes through modulas diviosn
                newRGB[c] = colorChange(pixel[c], int(base3NumStr[c]), 3)
                # https://pillow.readthedocs.io/en/3.2.x/reference/Image.html#PIL.Image.Image.putpixel
            myImage.putpixel((i,j),tuple(newRGB))
		    #IMPORTANT NOTE: Pillow likes to use tuples a lot
            indexForString +=  1

def unStegoImage(myImage):
    resultStr = ""
    # i is every pixel horizontally
    for i in range(myImage.size[0]):
	     # j is every pixel vertically
        for j in range(myImage.size[1]):
		    # https://pillow.readthedocs.io/en/3.2.x/reference/Image.html#PIL.Image.Image.getpixel
            pixel = myImage.getpixel((i,j))
            base3Array = [0,0,0]
            # this is a for loop that loops through the colors R G and B
            for c in range(0,3):
                base3Array[c] = int(pixel[c]) % 3
            base3String = ''.join(str(e) for e in base3Array)
            # if it is the end of the content
            if base3String == "222":
                return resultStr
            resultStr+=int2base(int(base3String,3),16)[-1]
		    #IMPORTANT NOTE: Pillow likes to use tuples a lot
    return resultStr


if len(sys.argv) != 2:
    print "please put file path"
    print "Usage: python encryptAndDecrypt.py <filepath>"
    sys.exit()
else:
    filename = sys.argv[1]

with open(filename) as f:
    content = f.read()
key = "abcabcabcabcabca"# the length has to be multiple of 16

#encrypt contents with file name
encrypted = encrypt(content+"^"+filename.split("/")[-1], key)
encryptedString = str(encrypted)

myImage = Image.open("100.bmp")

if len(encrypted) > myImage.size[0]* myImage.size[1]:
    print "error the data is too big"
    sys.exit()

#making stego image
stegoImage(myImage, encryptedString)
myImage.save("new.bmp")

#read new image and unstego it
newImage = Image.open("new.bmp")
hiddenData = unStegoImage(newImage)
print encryptedString
print hiddenData

decrypted = decrypt(hiddenData , key)
filename2 = decrypted.split("^")[-1]
writepath = 'decrypted/'+filename2
content2 =  decrypted[:-len(filename2)-1]

with open(writepath, 'w') as f:
    f.write(content2)
