from PIL import Image
im = Image.open("100.bmp")

pixel = im.getpixel((99,99))
pixel = (255,255,0)

im.putpixel((200,200), (0,0,0))

im.save("100.bmp")