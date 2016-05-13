from PIL import Image
myImage = Image.open("100.bmp")


def colorChange(currentColor, requestedVal, baseN):
    currentVal = currentColor % baseN
    distanceToNext = -1

    # color is already correct
    if currentVal == requestedVal:
        return currentColor

    # Color is 0
    if currentColor == 0:
        if requestedVal > 0:
            return requestedVal

    if currentVal < requestedVal:
        distanceToNext = requestedVal - currentVal
    else:
        distanceToNext = baseN - currentVal + requestedVal

    distanceToPrev = currentColor - requestedVal

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


for i in range(myImage.size[0]):
    for j in range(myImage.size[1]):
        pixel = myImage.getpixel((i,j))
        newRGB = [0,0,0]
        for c in range(0,3):
            newRGB[c] = colorChange(pixel[c], 2, 3)
        #print newRGB
        myImage.putpixel((i,j),tuple(newRGB))

myImage.save("new.bmp")