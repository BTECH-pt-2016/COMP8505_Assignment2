import sys
import os
from PIL import Image
from dcimage import *


KEY = ""
PATH_COVER_IMAGE = ""
PATH_STEGO_IMAGE = ""
PATH_FOLDER_EXTRACTED = "hiddenData/"
MODE = ""
PATH_TO_DATA = ""

USAGE = (
    "\nUSAGE:\n"
    "   To hide data:\n"
    "       python dcstego.py -s -p <password> -c <path_to_cover_image> -o <path_to_output_image> -d <path_to_data>\n"
    "       ex: python dcstego.py -s -p password -c 100.bmp -o stego/new.bmp -d samples/test.txt\n\n"
    "   To extract data:\n"
    "       python dcstego.py -e -p <password> -c <path_to_cover_image> \n"
    "       ex: python dcstego.py -e -p password -c stego/new.bmp \n\n\n"


    "SWITCHES:\n"
    "   -s  hide a data into a cover image\n"
    "   -e  extract a hidden data from a cover image\n"
    "   -p  password to hide or extract data\n"
    "   -c  set cover image path. Image has to be BMP\n"
    "   -o  set path for a stego image. The path has to end with .BMP\n"
    "   -d  set data to be hidden in cover image\n"
    "   -h  print usage\n"
    )


def parseArg():
    for i in range(1, len(sys.argv)):
        character = sys.argv[i][0]
        if character == "-":
            switch = sys.argv[i][1]
            if switch in {'s', 'e'}:
                global MODE
                MODE = switch
            elif switch == 'p':
                global KEY
                KEY = sys.argv[i+1]
            elif switch == 'c':
                global PATH_COVER_IMAGE
                PATH_COVER_IMAGE = sys.argv[i+1]
            elif switch == 'o':
                global PATH_STEGO_IMAGE
                PATH_STEGO_IMAGE = sys.argv[i+1]
            elif switch == 'd':
                global PATH_TO_DATA
                PATH_TO_DATA = sys.argv[i+1]
            elif switch == 'h':
                print USAGE
                return "done"

        else:
            continue

def validation():
    if KEY == "":
        print "please specify a password"
        return "done"

    if PATH_COVER_IMAGE == "":
        print "please specify a path to a cover image"
        return "done"
    else:
        name, ext = os.path.splitext(PATH_COVER_IMAGE)
        if ext != ".bmp":
            print "please set a BMP image for the cover image"
            return "done"

    if MODE == 's':
        if PATH_STEGO_IMAGE == "":
            print "please specify a path to an output image"
            return "done"
        else:
            name, ext = os.path.splitext(PATH_COVER_IMAGE)
            if ext != ".bmp":
                print "please set a BMP image for an output image"
                return "done"
        if PATH_TO_DATA == "":
            print "please specify a path to data to be hidden"
            return "done"

    elif MODE == 'e':
        return
    else:
        print "please specify the mode to use, hide or extract\n"
        return "done"

def embed(coverImage):
    #Open data file
    with open(PATH_TO_DATA) as f:
        content = f.read()
    #encrypt contents and file name with KEY
    encryptedString = encrypt(content+"^"+PATH_TO_DATA.split("/")[-1], KEY)
    #validation for image sizes
    if len(encryptedString) > coverImage.size[0]* coverImage.size[1]:
        print "Error: the data is too big for cover image. Please set bigger cover image or smaller data"
        sys.exit()
    #create stego image function is inside dcimage.py
    stegoImage(coverImage, encryptedString)
    coverImage.save(PATH_STEGO_IMAGE)
    print "Stego image is successfully saved to "+ PATH_STEGO_IMAGE

def extract(coverImage):
    #extract data from image
    hiddenData = unStegoImage(coverImage)
    #decrypt data
    decrypted = decrypt(hiddenData , KEY)
    #separate file name and contents from decrypted data
    filename = decrypted.split("^")[-1]
    writepath = PATH_FOLDER_EXTRACTED + filename
    content =  decrypted[:-len(filename)-1]

    if not os.path.exists(PATH_FOLDER_EXTRACTED):
        os.makedirs(PATH_FOLDER_EXTRACTED)
    #write content to the path
    with open(writepath, 'w') as f:
        f.write(content)
    print "Hidden data is successfully saved to "+ PATH_FOLDER_EXTRACTED + filename



def main():
    if parseArg() == "done":
        sys.exit()
    if validation() == "done":
        sys.exit()
    else:
        coverImage = Image.open(PATH_COVER_IMAGE)
        if MODE == 's':
            embed(coverImage)

        elif MODE == 'e':
            extract(coverImage)


if __name__ == '__main__':
	main()
