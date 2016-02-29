import Tkinter as tk
import ttk
import tkFileDialog
from os import path
import PIL
from PIL import Image, ImageTk
from filters import general
import utils.hist as hist
from utils import resize as rz

global_variables = {}

def init_screen():
    ipadding = 2

    #root window
    root = tk.Tk()
    global_variables['root_window'] = root
    root.resizable(0, 0)
    root.title("Super Awesome")

    ttk.Label(root, text="File:").grid(row=0, column=0, padx=ipadding, pady=ipadding)
    ttk.Button(root, text="Browse", command=getfilename).grid(row=0, column=1, padx = ipadding, pady=ipadding, ipadx=ipadding, ipady=ipadding, sticky='EW')
    root.mainloop()


def getfilename():
    indir = "../" + path.dirname(path.realpath(__file__))
    v = tkFileDialog.askopenfile(initialdir=indir)
    if v:
        global_variables['img_path'] = v.name
        main_window()


def main_window():
    global_variables['root_window'].destroy()
    main_gui_window = tk.Tk()
    #(global_variables['img_path'])

    img = Image.open(global_variables['img_path'])
    global_variables['working_image'] = rz.resize(img)
    img = rz.resize(img)
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(main_gui_window, image=photo)
    label.image = photo #IDEK why
    global_variables['image_label'] = label
    global_variables['gui_image'] = label.image
    label.grid(row = 0, column= 0, rowspan=12)
    tk.Button(main_gui_window, text="Convertir a escala de grises", command=convert_to_grayscale_gui).grid(row=0, column=1, sticky="NEWS")
    tk.Button(main_gui_window, text="Convertir a imagen Binaria", command=convert_to_binary_ask).grid(row=1, column=1, sticky="NEWS")
    tk.Button(main_gui_window, text="Invertir colores", command=invert_image_gui).grid(row=2, column=1, sticky="NEWS")

    tk.Button(main_gui_window, text="Ver Histograma", command=show_hist).grid(row=3, column=1, sticky="NEWS")


    main_gui_window.mainloop()

def show_hist():
    hist.hist(global_variables['working_image'])

def update_image(img):
    global_variables['working_image'] = img
    photo = ImageTk.PhotoImage(img)
    global_variables['image_label'].configure(image=photo)
    global_variables['image_label'].image = photo

def convert_to_grayscale_gui():
    img = general.convert_to_grayscale(global_variables['working_image'])
    update_image(img)


def convert_to_binary_gui():
    img = general.binary_threshold(global_variables['working_image'], int(global_variables['binary_scale'].get()))
    update_image(img)

def convert_to_binary_ask():
    option_pane = tk.Tk()
    tk.Label(option_pane, text="Select Threshold").pack()
    global_variables['binary_scale'] = tk.Scale(option_pane, from_=0, to=255, orient=tk.HORIZONTAL)
    global_variables['binary_scale'].pack()
    tk.Button(option_pane, text="Preview").pack()
    tk.Button(option_pane, text="Apply", command=convert_to_binary_gui).pack()



def invert_image_gui():
    img = general.invert_image(global_variables['working_image'])
    update_image(img)
