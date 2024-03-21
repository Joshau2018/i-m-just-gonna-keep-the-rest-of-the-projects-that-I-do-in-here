import tkinter as tk
from pathlib import Path
from tkinter import filedialog
import os

from PIL import ImageTk, Image

from PictureAdjuster import *

#WINDOW_HEIGHT = 600
#WINDOW_WIDTH = 840
CANVAS_FRAME_WIDTH = 400
CANVAS_FRAME_HEIGHT = 400
CANVAS_WIDTH = int(0.98 * CANVAS_FRAME_WIDTH)
CANVAS_HEIGHT = int(0.98 * CANVAS_FRAME_HEIGHT)
CONTROLS_WIDTH = CANVAS_FRAME_WIDTH + CANVAS_FRAME_HEIGHT
CONTROLS_HEIGHT = 180
WINDOW_HEIGHT = int((CONTROLS_HEIGHT + CANVAS_FRAME_HEIGHT) * 1.05)
WINDOW_WIDTH = int(2 * CANVAS_FRAME_WIDTH * 1.05)

# Only inherits the class of tk
class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Picture Adjuster")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.filename = ""
        self.path = ''
        self.img = None
        self.img_tk = None
        self.img_adjusted = None
        self.img_tk_adjusted = None

        self.pa = PictureAdjuster()

        self.__build_components()

    def __build_components(self):
        # Menu
        menu = tk.Menu()
        self.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.__browse_files)

        # Frames
        self.left_frame = tk.Frame(self, width=CANVAS_FRAME_WIDTH, height=CANVAS_FRAME_HEIGHT, bg="White",
                                   highlightcolor='black', highlightbackground='black', highlightthickness=3)
        self.left_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.right_frame = tk.Frame(self, width=CANVAS_FRAME_WIDTH, height=CANVAS_FRAME_HEIGHT, bg="White",
                                    highlightcolor='black', highlightbackground='black', highlightthickness=3)
        self.right_frame.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        self.control_frame = tk.Frame(self, width=CONTROLS_WIDTH, height=CONTROLS_HEIGHT, bg="White",
                                      highlightcolor='black', highlightbackground='black', highlightthickness=3)
        self.control_frame.grid(row=1, column=0, columnspan=2, sticky="s", padx=10, pady=5)
        self.buttons_frame = tk.Frame(self.control_frame, width=int(CONTROLS_WIDTH / 3 - 10),
                                      height=CONTROLS_HEIGHT - 20, bg="white", highlightbackground="black",
                                      highlightcolor="black", highlightthickness=1)
        self.buttons_frame.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.adjust_select_frame = tk.Frame(self.control_frame, width=int(CONTROLS_WIDTH / 3 - 10),
                                            height=CONTROLS_HEIGHT - 20, bg="white", highlightbackground="black",
                                            highlightcolor="black", highlightthickness=1)
        self.adjust_select_frame.grid(row=0, column=1, padx=5, pady=2)
        
        self.one_color_frame = tk.Frame(self.control_frame)
        self.one_color_frame.grid(row=0, column=2, sticky="e", padx=5, pady=2)

        # Buttons
        file_button = tk.Button(self.buttons_frame, text="Open File", command=self.__browse_files)
        file_button.grid(row=0, column=0, padx=20, pady=30)
        adjust_picture_button = tk.Button(self.buttons_frame, text="Adjust Picture", command=self.__adjust_picture)
        adjust_picture_button.grid(row=0, column=1, padx=20, pady=30)

        # Radio buttons to select adjustment type
        self.adjust_type_var = tk.StringVar(value="sepia")
        self.rb_sepia = tk.Radiobutton(self.adjust_select_frame, text="Sepia", variable=self.adjust_type_var,
                                       value="sepia", background="white", command=self.__hide_show_color_frame)
        self.rb_sepia.pack(padx=10, pady=2, anchor=tk.W)
        self.rb_grayscale = tk.Radiobutton(self.adjust_select_frame, text="Grayscale", variable=self.adjust_type_var,
                                           value="grayscale", background="white", command=self.__hide_show_color_frame)
        self.rb_grayscale.pack(padx=10, pady=2, anchor=tk.W)
        self.rb_negative = tk.Radiobutton(self.adjust_select_frame, text="Negative", variable=self.adjust_type_var,
                                          value="negative", background="white", command=self.__hide_show_color_frame)
        self.rb_negative.pack(padx=10, pady=2, anchor=tk.W)
        self.rb_washout = tk.Radiobutton(self.adjust_select_frame, text="Washout", variable=self.adjust_type_var,
                                         value="washout", background="white", command=self.__hide_show_color_frame)
        self.rb_washout.pack(padx=10, pady=2, anchor=tk.W)
        self.rb_onecolor = tk.Radiobutton(self.adjust_select_frame, text="One Color", variable=self.adjust_type_var,
                                          value="onecolor", background="white", command=self.__hide_show_color_frame)
        self.rb_onecolor.pack(padx=10, pady=2, anchor=tk.W)
        self.__hide_show_color_frame()

        # Canvas
        self.left_canvas = tk.Canvas(self.left_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightcolor="red",
                                     highlightbackground="red", highlightthickness=1) # self.left_frame at he begginng gives it a parrent frame
        self.left_image_container = self.left_canvas.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.left_canvas.grid(row=0, column=0)
        self.right_canvas = tk.Canvas(self.right_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightcolor="red",
                                      highlightbackground="red", highlightthickness=1)
        self.right_image_container = self.right_canvas.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.right_canvas.grid(row=0, column=0)

    def load_image_from_file(self, canvas, image_container):

        if len(self.filename) == 0:
            return

        self.open_image()
        self.img_tk = ImageTk.PhotoImage(self.img)
        canvas.itemconfig(image_container, image=self.img_tk)
        canvas.imgref = self.img_tk

    def load_adjusted_image(self, canvas, image_container):

        self.img_tk_adjusted = ImageTk.PhotoImage(self.img_adjusted)
        canvas.itemconfig(image_container, image=self.img_tk_adjusted)
        canvas.imgref = self.img_tk_adjusted


    def open_image(self):
        loaded_image = Image.open(self.filename)

        # image resize
        canvas_width = CANVAS_WIDTH
        canvas_height = CANVAS_HEIGHT
        image_width = loaded_image.width
        image_height = loaded_image.height
        if image_height < image_width:
            proportion = canvas_width / image_width
        else:
            proportion = canvas_height / image_height
        image_width = int(image_width * proportion)
        image_height = int(image_height * proportion)
        self.img = loaded_image.resize((image_width, image_height))

    def __browse_files(self):
        if len(self.path) == 0:
            self.path = Path.cwd()
        self.filename = filedialog.askopenfilename(initialdir=f"{self.path}", title="Select an image file", filetypes=[("all files", "*.*")])
        self.path = os.path.split(self.filename)[0]
        self.load_image_from_file(self.left_canvas, self.left_image_container)

    def __hide_show_color_frame(self):
        #print(self.adjust_type_var.get())
        if self.adjust_type_var.get() == "onecolor":
            self.one_color_frame = tk.Frame(self.control_frame, width=int(CONTROLS_WIDTH / 3 - 10),
                                            height=CONTROLS_HEIGHT - 20, bg="white", highlightbackground="black",
                                            highlightcolor="black", highlightthickness=1)
            self.one_color_frame.grid(row=0, column=2, sticky="e", padx=5, pady=2)
            # Radio buttons for one color
            self.color_type = tk.StringVar(value="red")
            self.rb_red = tk.Radiobutton(self.one_color_frame, text="Red", variable=self.color_type, value="red",
                                         background="white")
            self.rb_red.pack(padx=10, pady=4, anchor=tk.W)
            self.rb_green = tk.Radiobutton(self.one_color_frame, text="Green", variable=self.color_type, value="green",
                                           background="white")
            self.rb_green.pack(padx=10, pady=4, anchor=tk.W)
            self.rb_blue = tk.Radiobutton(self.one_color_frame, text="Blue", variable=self.color_type, value="blue",
                                          background="white")
            self.rb_blue.pack(padx=10, pady=4, anchor=tk.W)
        else:
            self.one_color_frame.grid_forget()

    def __adjust_picture(self):
        if self.img is not None:
            self.pa.image = self.img
            self.pa.convert_method = self.adjust_type_var.get()
            if self.adjust_type_var.get() == 'onecolor':
                self.pa.color_component = self.color_type.get()
            self.img_adjusted = self.pa.image
            self.load_adjusted_image(self.right_canvas, self.right_image_container)
        else:
            return


if "__main__" == __name__:
    app = AppWindow()
    app.mainloop()
