import tkinter as tk
from PIL import Image, ImageDraw

class SimpleInk2GoClone:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.image = Image.new("RGB", (500, 500), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.draw_line)

    def draw_line(self, event):
        self.canvas.create_line(event.x, event.y, event.x + 1, event.y + 1, fill="black")
        self.draw.line([event.x, event.y, event.x + 1, event.y + 1], fill="black")

    def run(self):
        self.root.mainloop()
        self.image.save("annotation.png")

if __name__ == "__main__":
    app = SimpleInk2GoClone()
    app.run()
