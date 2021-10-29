import tkinter as tk
from pathlib import Path

from PIL import Image
from PIL.ImageTk import PhotoImage


class CanvasDisplay:

    default_background_path = Path('default_bg.gif')

    def __init__(self, canvas):
        self._canvas = canvas

        self._brush_size = 5
        self._brush_color = "black"
        self._background_image = None

    def get_canvas(self):
        return self._canvas

    def reset(self):
        self._canvas.delete("all")
        if self._background_image is None:
            self.update_background_image()
            return

        self._canvas.create_image((int(self._background_image.width() / 2),
                                   int(self._background_image.height() / 2)),
                                  image=self._background_image)

    def update_background_image(self):
        if self._background_image is not None:
            self._canvas.create_image((int(self._background_image.width() / 2),
                                       int(self._background_image.height() / 2)),
                                      image=self._background_image)

        elif self.default_background_path.exists():
            image = Image.open(self.default_background_path)
            image = image.resize((int(self._canvas['width']), int(self._canvas['height'])))
            self._background_image = PhotoImage(image)
            self.update_background_image()

    def draw_line(self, x1, y1, x2, y2):
        self._canvas.create_line(x1, y1, x2, y2, fill=self._brush_color, width=self._brush_size)

    def get_resized_image(self, image):
        return PhotoImage(
            image.resize((
                self._canvas.winfo_width(),
                self._canvas.winfo_height())))

    def show_image(self, image):
        self._canvas.create_image((0, 0), anchor=tk.NW, image=image)

    def delete(self, obj):
        self._canvas.delete(obj)
