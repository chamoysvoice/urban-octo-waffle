from PIL import Image

def hist(img):
    freq = img.histogram()
    h = Image.new('RGB', (256, 256), "black")
    avg = sum(freq) / len(freq)
    for y in xrange(h.size[1]):
        for x in xrange(h.size[0]):
            if freq[y] * 256 / avg > x :
                c = 255
            else:
                c = 0
            h.putpixel((255 - y, 255 - x),  (c, c, c))
    h.show()
