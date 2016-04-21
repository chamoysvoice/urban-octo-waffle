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

def neighborhoods(image, threshold):
    size = image.size
    tag = 0
    x = y = 0
    tags_matrix = [[0 for a in range(size[0])] for b in range(size[1])]         #Inicialmente llena de ceros (no hay vecindarios)
    neighbors_dictionary = {
        0: (x + 1, y),      #right neighbor
        1: (x, y + 1),      #bottom neighbor
        2: (x - 1, y),      #left neighbor
        3: (x, y - 1)       #top neighbor
    }
    while any(0 in t for t in tags_matrix):
        tag += 1    #Empieza una nueva vecindad
        tags_matrix[x][y] = tag     #El pixel actual se agrega a la vecindad
        has_neighbor = True
        while has_neighbor:
            pixel = image.getpixel((x, y))[0]
            try:
                right = image.getpixel(neighbors_dictionary[0])[0]
            except IndexError:
                right = 1000            #Se le asigna un valor muy alto para que no sobrepase el umbral cuando se revise
            try:
                bottom = image.getpixel(neighbors_dictionary[1])[0]
            except IndexError:
                bottom = 1000
            try:
                left = image.getpixel(neighbors_dictionary[2])[0]
            except IndexError:
                left = 1000
            try:
                top = image.getpixel(neighbors_dictionary[3])[0]
            except IndexError:
                top = 1000
            neighborhood = [right, bottom, left, top]   #Lista con los pixeles adyacentes
            for index in xrange(len(neighborhood)):
                coords = neighbors_dictionary[index]    #coordenadas del pixel adyacente que se va a revisar
                #Si el pixel adyacente no sobrepasa el umbral para considerlo como vecino
                if abs(pixel - neighborhood[index]) <= threshold:
                    #Si el pixel adyacente no pertence a un vecindario
                    if tags_matrix[coords[0]][coords[1]] == 0:
                        print str(x) + ", " + str(y) + " es vecino de: " + str(coords)
                        tags_matrix[coords[0]][coords[1]] = tag     #Se agrega el pixel vecino a la vecindad
                        x = coords[0]
                        y = coords[1]                           #El siguiente pixel a revisar sera el que recie fue agregado a la vecindad
                        neighbors_dictionary = {
                            0: (x + 1, y),
                            1: (x, y + 1),
                            2: (x - 1, y),
                            3: (x, y - 1)
                        }   #actualiza neighbors_dictionary con las coordenadas de los pixels adyacentes del siguiente pixel a revisar
                        print "Siguiente pixel: " + str(coords)
                        has_neighbor = True
                        break
                    elif index == 3:        #Si los 4 pixeles adyacentes son su vecinos pero ya estan en un vecindario
                        tags_matrix[x][y] = tags_matrix[coords[0]][coords[1]]   #Se agrega el pixel actual al mismo vecindario que tienen sus pixeles adyacentes
                        has_neighbor = False
                elif coords[0] in xrange(size[0]) and coords[1] in xrange(size[1]):     #Si la coordena existe en la imagen
                    next_coords = coords    #El siguiente pixel sera la primer incidencia donde no se encontro vecindad
                if index == 3:
                    print str(x) + ", " + str(y) + " no tiene vecinos!!!!!!!!"
                    has_neighbor = False    #No se encontro ningun vecino
                    print "Siguiente pixel a revisar: " + str(next_coords)
        x = next_coords[0]
        y = next_coords[1]
        neighbors_dictionary = {
            0: (x + 1, y),
            1: (x, y + 1),
            2: (x - 1, y),
            3: (x, y - 1)
        }   #actualiza neighbors_dictionary con las coordenadas de los pixels adyacentes del siguiente pixel a revisar
        print "sigue habiendo 0s"
        print "Vecindades: " + str(tag)
    f = open("/home/omar/Downloads/urban-octo-waffle/vecindades/output_files/matriz_vecindades.txt", "w")
    for m in xrange(size[0]):
        for n in xrange(size[1]):
            f.write(str(tags_matrix[m][n]) + " ")
        f.write("\n")
    f.close()
    colors = int(256 / tag)
    for height in xrange(size[1]):
        for width in xrange(size[0]):
            color = (tags_matrix[width][height] * colors) - 1
            image.putpixel((width, height), (color, color, color))
    print "Termine"
    return image
