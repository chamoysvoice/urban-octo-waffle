import PIL

def resize(img):
    size = 800
    if img.size[0] > size:
        basewidth = size
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        return img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    return img
