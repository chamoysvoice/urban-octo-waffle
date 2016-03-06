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
    main_gui_window.title(global_variables['img_path'])
    img = Image.open(global_variables['img_path'])
    global_variables['working_image'] = rz.resize(img)
    img = rz.resize(img)
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(main_gui_window, image=photo)
    label.image = photo #IDEK why
    global_variables['image_label'] = label
    global_variables['gui_image'] = label.image
    label.grid(row = 0, column= 0, rowspan=12)

    # -- Menu -- #
    menu = tk.Menu(main_gui_window)
    main_gui_window.config(menu=menu)
    # -- Main Submenu -- #
    mainMenu = tk.Menu(menu)
    mainMenu.add_command(label="Open file", command=main_gui_window.destroy)
    mainMenu.add_command(label="Save file", command=savefile)
    mainMenu.add_separator()
    mainMenu.add_command(label="Exit", command=main_gui_window.destroy)
    menu.add_cascade(menu=mainMenu, label="Menu")

    # -- Filters Submenu -- #
    filtersMenu = tk.Menu(menu)
    filtersMenu.add_command(label="Grayscale", command=convert_to_grayscale_gui)
    filtersMenu.add_command(label="To Binary", command=convert_to_binary_ask)
    filtersMenu.add_command(label="Invert Image", command=invert_image_gui)
    filtersMenu.add_command(label="Change Bright", command=change_bright_ask)
    filtersMenu.add_command(label="Stretch Contrast", command=stretch_contrast_ask)
    filtersMenu.add_command(label="Clear image", command=clear_ask)
    menu.add_cascade(menu=filtersMenu, label="Filters")

    # -- Tools Submenu-- #
    toolsMenu = tk.Menu(menu)
    toolsMenu.add_command(label="Plot Histogram", command=show_hist)
    menu.add_cascade(menu=toolsMenu, label="Tools")

    # -- MainLoop -- #
    main_gui_window.mainloop()


def show_hist():
    hist.hist(global_variables['working_image'])


def update_image(img):
    global_variables['working_image'] = img
    photo = ImageTk.PhotoImage(img)
    global_variables['image_label'].configure(image=photo)
    global_variables['image_label'].image = photo

def savefile():
    indir = "../" + path.dirname(path.realpath(__file__))
    output = tkFileDialog.asksaveasfilename(filetypes=[('PNG', '.png'), ('JPG', '.jpg')], initialfile='newfile', initialdir=indir)
    if output:
        global_variables['working_image'].save(output)

def convert_to_grayscale_gui():
    img = general.convert_to_grayscale(global_variables['working_image'])
    update_image(img)


def convert_to_binary_gui():
    threshold_binary = int(global_variables['binary_scale'].get())
    img = general.binary_threshold(global_variables['working_image'], thresh=threshold_binary)
    update_image(img)

def preview_to_binary_gui():
    threshold_binary = int(global_variables['binary_scale'].get())
    img = general.binary_threshold(global_variables['working_image'].copy(), thresh=threshold_binary)
    img.show()

def convert_to_binary_ask():
    option_pane = tk.Tk()
    tk.Label(option_pane, text="Select Threshold").pack()
    global_variables['binary_scale'] = tk.Scale(option_pane, from_=0, to=255, orient=tk.HORIZONTAL)
    global_variables['binary_scale'].pack()
    tk.Button(option_pane, text="Preview", command=preview_to_binary_gui).pack(side=tk.LEFT)
    tk.Button(option_pane, text="Apply", command=convert_to_binary_gui).pack(side=tk.LEFT)


def invert_image_gui():
    img = general.invert_image(global_variables['working_image'])
    update_image(img)


def change_bright_ask():

    option_pane = tk.Tk()
    tk.Label(option_pane, text="Select Threshold").pack()
    global_variables['bright_scale'] = tk.Scale(option_pane, from_=-255, to=255, orient=tk.HORIZONTAL)
    global_variables['bright_scale'].pack()
    tk.Button(option_pane, text="Preview", command=preview_change_bright).pack(side=tk.LEFT)
    tk.Button(option_pane, text="Apply", command=change_bright_gui).pack(side=tk.LEFT)
def preview_change_bright():
    value = int(global_variables['bright_scale'].get())
    img = general.change_brightness(global_variables['working_image'].copy(), value)
    img.show()

def change_bright_gui():
    value = int(global_variables['bright_scale'].get())
    img = general.change_brightness(global_variables['working_image'], value)
    update_image(img)

def stretch_contrast_ask():
    option_pane = tk.Tk()
    tk.Label(option_pane, text="Select Beta").pack()
    global_variables['contrast_beta'] = tk.Scale(option_pane, from_=-1, to=1, resolution=0.01, orient=tk.HORIZONTAL)
    global_variables['contrast_beta'].pack()
    tk.Label(option_pane, text="Select Gamma").pack()
    global_variables['contrast_gamma'] = tk.Scale(option_pane, from_=-255, to=255, orient=tk.HORIZONTAL)
    global_variables['contrast_gamma'].pack()
    tk.Button(option_pane, text="Preview", command=preview_stretch_contrast).pack(side=tk.LEFT)
    tk.Button(option_pane, text="Apply", command=stretch_contrast_gui).pack(side=tk.LEFT)

def preview_stretch_contrast():
    beta = float(global_variables['contrast_beta'].get())
    gamma = int(global_variables['contrast_gamma'].get())
    img = general.stretch_contrast(global_variables['working_image'].copy(), beta, gamma)
    img.show()

def stretch_contrast_gui():
    beta = float(global_variables['contrast_beta'].get())
    gamma = int(global_variables['contrast_gamma'].get())
    img = general.stretch_contrast(global_variables['working_image'], beta, gamma)
    update_image(img)

def clear_ask():
    option_pane = tk.Tk()
    tk.Label(option_pane, text="Select minimum luminance").pack()
    global_variables['clear_minimum_luminance'] = tk.Scale(option_pane, from_=0, to=255, orient=tk.HORIZONTAL)
    global_variables['clear_minimum_luminance'].pack()
    tk.Label(option_pane, text="Select maximum luminance").pack()
    global_variables['clear_maximum_luminance'] = tk.Scale(option_pane, from_=0, to=255, orient=tk.HORIZONTAL)
    global_variables['clear_maximum_luminance'].pack()
    tk.Button(option_pane, text="Preview", command=preview_clear).pack(side=tk.LEFT)
    tk.Button(option_pane, text="Apply", command=clear_gui).pack(side=tk.LEFT)

def preview_clear():
    min_luminance = int(global_variables['clear_minimum_luminance'].get())
    max_luminance = int(global_variables['clear_maximum_luminance'].get())
    img = general.clear(global_variables['working_image'].copy(), min_luminance, max_luminance)
    img.show()

def clear_gui():
    min_luminance = int(global_variables['clear_minimum_luminance'].get())
    max_luminance = int(global_variables['clear_maximum_luminance'].get())
    img = general.clear(global_variables['working_image'], min_luminance, max_luminance)
    update_image(img)
