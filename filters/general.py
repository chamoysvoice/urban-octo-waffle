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

# def change_brightness(image, amount):
#     if(amount > 255):
#         amount = 255
#     elif(amount < -255):
#         amount = -255
#     size = image.size
#
#     min_val = 255
#     max_val = 0
#
#     for x in xrange(size[0]):
#         for y in xrange(size[1]):
#             pixel = image.getpixel((x,y))
#             if pixel[0] > max_val:
#                 max_val = pixel[0]
#             if pixel[0] < min_val:
#
