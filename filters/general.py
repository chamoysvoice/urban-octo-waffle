def binary_threshold(image, thresh=128):
    if thresh > 1:
        thresh /= 255.0
    size = image.size
    print thresh
    for x in xrange(size[0]):
       for y in xrange(size[1]):
           pixel = image.getpixel((x, y))
           if(pixel[0] < (255 * thresh)):
               pixel = (0, 0, 0)
           else:
               pixel = (255, 255, 255)
           image.putpixel((x, y), pixel)
    return image

def convert_to_grayscale(image, debug=False, printable=False):
    size = image.size
    if printable:
        step = size[0] / 10
    for x in xrange(size[0]):
        for y in xrange(size[1]):
            pixel = image.getpixel((x,y))
            g = (pixel[0] + pixel[1] + pixel[2]) / 3
            image.putpixel((x, y), (g, g, g))
        if printable and x % step == 0:
            print '.',
    if printable:
        print
    return image

def invert_image(image, debug=False, printable=False):
    size = image.size
    if printable:
        step = size[0] / 10
    for x in xrange(size[0]):
        for y in xrange(size[1]):
            pixel = image.getpixel((x,y))
            ir = pixel[0]
            ig = pixel[1]
            ib = pixel[2]
            image.putpixel((x, y), (255 - ir, 255 - ig, 255 - ib))
        if printable and x % step == 0:
            print '.',
    if printable:
        print
    return image

def change_brightness(image, value):
    size = image.size
    for x in xrange(size[0]):
        for y in xrange(size[1]):
            pixel = image.getpixel((x, y))
            v = min(pixel[0] + value, 255)
            v = max(0, v)
            image.putpixel((x, y), (v, v, v))
    return image

def stretch_contrast(image, beta, gamma):
    size = image.size
    for x in xrange(size[0]):
        for y in xrange(size[1]):
            pixel = image.getpixel((x, y))
            P0 = int(pixel[0] * beta + gamma)
            P0 = min(P0, 255)
            P0 = max(0, P0)
            image.putpixel((x, y), (P0, P0, P0))
    return image

def clear(image, min_luminance, max_luminance):
    size = image.size
    for x in xrange(size[0]):
        for y in xrange(size[1]):
            pixel = image.getpixel((x, y))
            P0 = max(pixel[0], min_luminance)
            P0 = min(pixel[0], max_luminance)
            image.putpixel((x, y), (P0, P0, P0))
    return image

def median(image):
    size = image.size
    for x in xrange(1, size[0] - 1):
        for y in xrange(1, size[1] - 1):
            n = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 and dy != 0:
                        n.append(image.getpixel((x + dx, y + dy))[0])
            max_p = max(n)
            min_p = min(n)
            if(image.getpixel((x, y))[0] < min_p):
                i = min_p
            elif(image.getpixel((x, y))[0] > max_p):
                i = max_p
            else:
                i = image.getpixel((x, y))[0]
            image.putpixel((x, y), (i, i, i))
    #debug
    print "Median Filter"
    return image

def mean(image):
    size = image.size
    for x in xrange(1, size[0] - 1):
        for y in xrange(1, size[1] - 1):
            n = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    n.append(image.getpixel((x + dx, y + dy))[0])
            i = sum(n) / len(n)
            image.putpixel((x, y), (i, i, i))
    #debug
    print "Mean Filter"
    return image

def salt_pepper(image):
    size = image.size
    for x in xrange(1, size[0] - 1):
        for y in xrange(1, size[1] - 1):
            n = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    n.append(image.getpixel((x + dx, y + dy))[0])
            center = n[4]
            del n[4]
            if abs(center - (sum(n) / len(n))) > 60:
                i = sum(n) / len(n)
            else:
                i = center
            image.putpixel((x, y), (i, i, i))
    #debug
    print "Salt Pepper Filter"
    return image
