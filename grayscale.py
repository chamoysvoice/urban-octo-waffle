from PIL import Image
from filters.general import binary_threshold, convert_to_grayscale

def main():
    im = Image.open('images/cat.jpg')
    print "Preparando la imagen"
    im = convert_to_grayscale(im, printable=True)
    threshold = int(raw_input("Entra el umbral -> "))
    im = binary_threshold(im, threshold)
    im.show()

if __name__ == '__main__':
    main()

