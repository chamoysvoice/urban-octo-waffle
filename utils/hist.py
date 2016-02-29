from PIL import Image

def hist(img):
    freq = img.histogram()
    h = Image.new('RGB', (256, 256), "black")
    avg = sum(freq) / len(freq)
    c = [0, 0, 0]
    for y in xrange(h.size[1]):
        for x in xrange(h.size[0]):
            for k in xrange(len(c)):
                if freq[y + (256 * k)] * 256 / (avg * 1.5) > x :
                    c[k] = min(128 + x / 2, 255)
                else:
                    c[k] = 0
            h.putpixel((y, 255 - x),  (c[0], c[1], c[2]))
    h.show()
