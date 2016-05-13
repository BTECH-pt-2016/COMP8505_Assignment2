from PIL import Image
from encryptAndDecrypt import *



myImage = Image.open("100.bmp")

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
    distanceToPrev = currentColor - requestedVal

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

encryptedString = str(encrypted)

max = len(encryptedString)
indexForString = 0
# i is every pixel horizontally
for col in range(myImage.size[0]):
	# j is every pixel vertically
    for row in range(myImage.size[1]):
		# https://pillow.readthedocs.io/en/3.2.x/reference/Image.html#PIL.Image.Image.getpixel
        pixel = myImage.getpixel((col,row))
        newRGB = [0,0,0]
        base3NumStr = str(int(int2base(int(encryptedString[indexForString],16),3)))
        base3NumStr = "{:0>3}".format(base3NumStr)
		# this is a for loop that loops through the colors R G and B
        # going backwords 2,1,0
        for c in range(2,-1,-1):
			# below im requesting the nearest color to achieve "2" in base 3.
			# NOTE: colorChange returns the colorValue which will produce the value "2" once it goes through modulas diviosn
            newRGB[c] = colorChange(pixel[c], int(base3NumStr[c]), 3)
        # https://pillow.readthedocs.io/en/3.2.x/reference/Image.html#PIL.Image.Image.putpixel
        myImage.putpixel((col,row),tuple(newRGB))
		#IMPORTANT NOTE: Pillow likes to use tuples a lot

        indexForString +=  1
        if(max <= indexForString):
            # save the modified image
            print "%d in %d" % ( myImage.size[0] , col)
            print "%d in %d" % ( myImage.size[1] , row)

            myImage.save("new.bmp")
            sys.exit()
