from ..label import IqaData, Rois0123Label, cached_property
from pathlib import Path
import os, io
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk # put it after tkinter to overwrite tkinter.Image
import numpy as np  # np.roll

"""
# %% browse one database
from fastiqa.gui import *; Browser(CLIVE)

# NOTE: exit to run next browser
Browser(KonIQ)
Browser(FLIVE)
Browser(FLIVE640)

# %% browse multiple database at the same time
from fastiqa.gui import *; Browser(FLIVE640) + Browser(CLIVE) + Browser(KonIQ)
"""

class Browser(IqaData):
    pred = None
    fn = None
    img = None
    tk_img = None
    canvas = None
    _index = 0
    percent = 1  # 100%
    cfg_rectangle = {}
    hide_scores = False
    opt_bbox_width = [4, 0, 1]
    out_dir = Path('')
    df_view = None

    def __init__(self, label, **kwargs):
        super().__init__(label, **kwargs)
        self.opt_label_suffixes = self.label_suffixes
        self.__dict__.update(kwargs)

    def __add__(self, other):
        other.window = Toplevel(master=self.window)
        other.load_frame()
        return self

    def load_frame(self):
        self.reload()
        self.frame = Frame(self.window, width=500, height=400, bd=1)
        self.frame.pack()
        self.frame.bind("<Key>", self.on_key)  # canvas covered by image don't response to key press...
        self.frame.bind("<Left>", self.prev)
        self.frame.bind("<Right>", self.next)
        self.frame.bind("<Up>", self.prev_mode)
        self.frame.bind("<Down>", self.next_mode)
        self.frame.bind("<Escape>", self.exit)
        self.canvas = Canvas(self.frame)
        self.canvas.bind("<Button-1>", self.callback)
        self.frame.focus_set()
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.show()

    @cached_property
    def window(self):
        return Tk()

    def _repr_html_(self):
        self.load_frame()
        return self.window.mainloop()

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = int(value) % len(self.df_view)

    def show(self):
        # suffix
        # zscore? prefix
        #
        def add_bbox(suffix):
            x1, x2 = self.df_view['left' + suffix][self.index], self.df_view['right' + suffix][self.index]
            y1, y2 = self.df_view['top' + suffix][self.index], self.df_view['bottom' + suffix][self.index]

            color = 'lightgreen' if suffix == self.opt_label_suffixes[0] else 'yellow'
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=self.opt_bbox_width[0], **self.cfg_rectangle)

            if not self.hide_scores:
                # TODO self.label_cols[0]   mos or zscore (add score_mode)
                # show all predictions?  mos, zscore, pred
                s = f"{self.df_view[self.label_types[0] + suffix][self.index]:.1f}"
                if suffix is '_image' and self.pred is not None:
                    s = f"Actual: {s} / Predication: {self.pred:.1f}"  # load from the table!!!!
                text = self.canvas.create_text((x1, y1), anchor=NW, text=s)
                r = self.canvas.create_rectangle(self.canvas.bbox(text), fill=color, outline=color)
                self.canvas.tag_lower(r, text)

        self.fn = self.df_view[self.fn_col][self.index]
        file = self.path / self.folder / self.fn
        self.img = self.open_image(file)
        width, height = self.img.size
        # PIL image
        self.tk_img = ImageTk.PhotoImage(self.img)
        # tk_img = ImageTk.PhotoImage(im)
        # self.canvas.itemconfig(self.image_on_canvas, image=tk_img)
        # then it will be optimized, showing nothing

        self.canvas.delete("all")
        self.canvas.config(width=width, height=height)

        self.canvas.create_image(0, 0, image=self.tk_img, anchor=NW)

        # only for Rois0123Label
        # if isinstance(self.label, Rois0123Label):
        for suffix in self.label_suffixes:
            add_bbox(suffix)
        # add_bbox('_image')
        # add_bbox('_patch_1')
        # add_bbox('_patch_2')
        # add_bbox('_patch_3')

        # self.image_on_canvas =
        # self.canvas.itemconfig(self.image_on_canvas, image=self.tk_img)
        #
        # self.canvas.coords(self.patch1_on_canvas,
        #                    self.df_view.left_patch_1[self.index],
        #                    self.df_view.top_patch_1[self.index],
        #                    self.df_view.right_patch_1[self.index],
        #                    self.df_view.bottom_patch_1[self.index],
        #                    )

        self.canvas.pack()
        fn = self.df_view[self.fn_col][self.index]
        self.window.title(f'[{width}x{height}]({self.index + 1}/{len(self.df_view)}: {self.percent * 100:.2f}%) {fn}')

    # some API to custom your browser
    def open_image(self, file):
        """

        :param file:
        :return: a PIL image
        """
        return Image.open(file)  # "../data/FLIVE/EE371R/cj23478+019.jpg"
        # if self.apply_img_proc: im = self.img_proc(im)


    def prev(self, event=None):
        self.index -= 1
        self.show()

    def next(self, event=None):
        self.index += 1
        self.show()

    def prev_mode(self, event=None):
        self.opt_label_suffixes = np.roll(self.opt_label_suffixes, -1)
        self.show()

    def next_mode(self, event=None):
        self.opt_label_suffixes = np.roll(self.opt_label_suffixes, 1)
        self.show()

    # def reset(self, event):
    #     self.valid_mos = None

    def exit(self, event=None):
        self.window.destroy()

    def filter(self, func):
        df = self.df_view[func(self.df_view)]
        if len(df) == 0:
            messagebox.showwarning("Warning", "No image found!")
        else:
            self.percent = len(df) / len(self.df_view)
            self.df_view = df.reset_index()  # otherwise index 0 will be dropped
            self._index = 0
        self.show()
        return self

    def save_image(self):
        # self.grab_image(self.canvas).save(self.fn)
        # https://stackoverflow.com/questions/41940945/saving-canvas-from-tkinter-to-file?rq=1
        ps = self.canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(self.out_dir / self.fn.rsplit('/', 1)[1], 'jpeg')

    def reload(self):
        self.df_view = self.df

    def on_key(self, event):
        self.frame.focus_set()
        # print("pressed", repr(event.char))
        if event.char in [str(n) for n in range(10)]:
            self.reload()
            col_name = self.label_types[0] + self.opt_label_suffixes[0]
            # there might not be valid data
            self.filter(lambda x: x[col_name] // 10 == int(event.char))

        elif event.char is ' ':
            self.reload()
            self.show()
        elif event.char is 's':  # save capture
            self.save_image()

        elif event.char is 'h':  # hide score
            self.hide_scores = not self.hide_scores
            self.show()
        elif event.char is 'w':  # i
            self.opt_bbox_width = np.roll(self.opt_bbox_width, 1)
            self.show()
        else:
            pass
        # print(self.index)



    # https://stackoverflow.com/questions/9886274/how-can-i-convert-canvas-content-to-an-image
    # def grab_image(self, widget):
    #     x = self.window.winfo_rootx() + widget.winfo_x()
    #     y = self.window.winfo_rooty() + widget.winfo_y()
    #     x1 = x + widget.winfo_width()
    #     y1 = y + widget.winfo_height()
    #     return ImageGrab.grab().crop((x, y, x1, y1))
    #     # .save(filename)

    def callback(self, event):
        self.frame.focus_set()
        print("clicked at", event.x, event.y)
        print(self.df_view[self.fn_col][self.index])






"""
WontFix
* support different backend: tkinter or matplotlib

Reference
=========

https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

Matplotlib backbone
===================

https://matplotlib.org/gallery/animation/image_slices_viewer.html


PySimpleGUI
============

PySimpleGUI is a wrapper for Tkinter and Qt (others on the way). The amount of code required to implement custom GUIs is much shorter using PySimpleGUI than if the same GUI were written directly using Tkinter or Qt.

sudo apt-get install python-tk
sudo apt-get install python3-tk

https://github.com/PySimpleGUI/PySimpleGUI

not working here, cannot switch images

Tkinter
========

sudo apt-get install python3.6-tk


wont support python 2
for browser only, support python 2

import sys
if sys.version_info[0] == 3:
    # for Python3
    from tkinter import *
    # print(TclVersion)
else:
    # for Python2
    from Tkinter import *

"""
