# responsible for the image processing

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import datetime

fontPath = "fonts/arial.ttf"


class Canvas:
    """
       make(width, height, color, text size, margin)
       default constructor (image picture, text size, margin)
    """

    def __init__(self, img, t_size, margin):
        self.canvas = img
        self.margin = margin
        self.text_size = t_size
        self.items = []
        self.x = margin
        self.y_pos = 0
        self.gap = t_size / 2
        self.font = ImageFont.truetype(fontPath, self.text_size)
        self.lastRowIndex = 0

    # pass in custom width and height, text size and margin to create a canvas
    @classmethod
    def make(cls, width, height, BGcolor):
        size = int(height / 20)
        margin = int(size * 0.75)
        canvas = Image.new("RGB", (width, height), BGcolor)
        return cls(canvas, size, margin)

    # open a new picture as the background and the text size and margin would be determined automatically
    @classmethod
    def open(cls, direct):
        im = Image.open(direct)
        size = int(im.height / 20)
        margin = int(size * 0.75)
        return cls(im, size, margin)

    def getContent(self):
        return self.items

    def display(self):
        self.canvas.show()

    def addItemTo(self, text):
        self.items.append(text)
        if not self.y_pos:
            self.y_pos = self.margin  # starting position:  y = 50
        else:
            self.y_pos = (self.y_pos + self.gap + self.text_size / 2)
            if self.y_pos > self.canvas.height:  # if the item passes beyond the height
                self.y_pos = self.margin  # go back to the starting position:  y = 50
                maxLen = len(max(self.items[self.lastRowIndex:], key=len))
                offset = maxLen * self.text_size + 10
                self.x += offset
                self.lastRowIndex = len(self.items)

        draw = ImageDraw.Draw(self.canvas)
        # coordinate
        draw.text((self.x, self.y_pos),
                  self.items[-1], (255, 255, 255), font=self.font)

    def addDate(self):
        size = int(0.8 * self.text_size)
        draw = ImageDraw.Draw(self.canvas)
        date_font = ImageFont.truetype(fontPath, size)
        date = str(datetime.date.today())
        draw.text((self.canvas.width - len(date) * size / 2 - self.margin,
                  self.margin), date, (255, 255, 255), font=date_font)

    def export(self, path):
        time = str(datetime.datetime.now())
        time = time[:19].replace(" ", "_")
        dest_dir = path + '/' + time + ".png"
        self.canvas.save(dest_dir)
