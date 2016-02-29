from PIL import Image
import grayscale
import glob, os

#abrir una imagen
im = Image.open('images/cat.jpg')

#Obtener el tamanio de los pixeles <- no usar letras especiales como "enie" ni acentos
size = im.size
print "Size: " + str(size)



#Obtener un pixel
pixel20_40 = im.getpixel((20, 40))  # (20, 40) es una tupla
print "Pixel (20, 40) =>" + str(im.getpixel((20, 40)))

#Obtener los canales :)
print "Red Channel => " + str(pixel20_40[0])  # 0 = rojo
print "Green Channel => " + str(pixel20_40[1])  # 1 = verde
print "Blue Channel => " + str(pixel20_40[2])  # 2 = azul

#hacer un pixel negro (r, g, b) [Es una tupla]
pixel_negro = (0,0,0)

#escribir el pixel en la imagen en la posicion 30, 50
pos = (30, 50)
im.putpixel(pos, pixel_negro)

#mostrar la imagen
im.show()

for infile in glob.glob("images/*.jpg"):
    file, ext  = os.path.splitext(os.path.split(infile)[1])
    im = Image.open(infile, 'r')
    im = im.convert("L")
    im.show()
    im.thumbnail((128,128), Image.ANTIALIAS)
    im.save("thumbnail/" + file + ".thumbnail.jpg", "JPEG")

#proceso de algo
grayscale.main()
#proceso de algo mas