import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import random

# Color helpers
r = lambda: random.randint(50, 255)
rc = lambda: ('#%02X%02X%02X' % (r(), r(), r()))

def create_invader(border, draw, size):
    x0, y0, x1, y1 = border
    square_size = (x1 - x0) / size
    rand_colors = [rc(), rc(), rc(), '#000000', '#000000', '#000000']

    for y in range(size):
        row = []
        for x in range((size + 1) // 2):  # half the row
            color = random.choice(rand_colors)
            row.append(color)
        mirrored_row = row + row[::-1] if size % 2 == 0 else row + row[-2::-1]
        for x in range(size):
            color = mirrored_row[x]
            draw.rectangle((x * square_size + x0, y * square_size + y0,
                            x * square_size + x0 + square_size, y * square_size + y0 + square_size),
                           fill=color)

def generate_sheet(size, invaders, imgSize):
    image = Image.new('RGB', (imgSize, imgSize), 'white')
    draw = ImageDraw.Draw(image)
    invaderSize = imgSize / invaders
    padding = invaderSize / size
    for ix in range(invaders):
        for iy in range(invaders):
            x0 = ix * invaderSize + padding
            y0 = iy * invaderSize + padding
            x1 = x0 + invaderSize - 2 * padding
            y1 = y0 + invaderSize - 2 * padding
            create_invader((x0, y0, x1, y1), draw, size)
    return image

class App:
    def __init__(self, root):
        self.root = root
        root.title("Invader Sprite Preview with Tabs and Generations")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Store latest image from Tab 1 generate
        self.last_generated_image = None

        self.tab1 = self.build_tab(evolution_mode=False)
        self.notebook.add(self.tab1, text="Generate Single")

        self.tab2 = self.build_tab(evolution_mode=True)
        self.notebook.add(self.tab2, text="Batch / Evolution")

    def build_tab(self, evolution_mode=False):
        frame = tk.Frame(self.notebook)

        ctrl = tk.Frame(frame)
        ctrl.pack(side='top', fill='x', padx=10, pady=10)

        tk.Label(ctrl, text="Grid Size (pixels per invader):").grid(row=0, column=0, sticky='w')
        size_slider = tk.Scale(ctrl, from_=3, to=20, orient='horizontal')
        size_slider.set(8)
        size_slider.grid(row=0, column=1, sticky='we')

        tk.Label(ctrl, text="Invaders per row:").grid(row=1, column=0, sticky='w')
        inv_slider = tk.Scale(ctrl, from_=1, to=10, orient='horizontal')
        inv_slider.set(5)
        inv_slider.grid(row=1, column=1, sticky='we')

        tk.Label(ctrl, text="Canvas Size (px):").grid(row=2, column=0, sticky='w')
        img_slider = tk.Scale(ctrl, from_=100, to=2000, resolution=50, orient='horizontal')
        img_slider.set(500)
        img_slider.grid(row=2, column=1, sticky='we')

        if evolution_mode:
            tk.Label(ctrl, text="Number of generations:").grid(row=3, column=0, sticky='w')
            gen_entry = tk.Entry(ctrl, width=10)
            gen_entry.insert(0, "10")
            gen_entry.grid(row=3, column=1, sticky='w')
        else:
            gen_entry = None

        canvas = tk.Canvas(frame, width=500, height=500, bg='grey')
        canvas.pack(padx=10, pady=10)
        canvas.image_ref = None

        def generate_single_image():
            size = int(size_slider.get())
            inv = int(inv_slider.get())
            imgS = int(img_slider.get())
            return generate_sheet(size, inv, imgS)

        def update_preview():
            if not evolution_mode:
                # Tab 1: just generate once and display
                img = generate_single_image()
                self.last_generated_image = img
                show_image(img)
            else:
                # Tab 2: animate generations one by one
                try:
                    generations = int(gen_entry.get())
                except Exception:
                    generations = 10

                current_gen = 0

                def generate_next_gen():
                    nonlocal current_gen
                    if current_gen < generations:
                        img = generate_single_image()
                        self.last_generated_image = img
                        show_image(img)
                        current_gen += 1
                        # schedule next generation after 300ms (adjust for speed)
                        canvas.after(300, generate_next_gen)

                generate_next_gen()

        def show_image(img):
            img_tk = ImageTk.PhotoImage(img)
            canvas.config(width=img.width, height=img.height)
            canvas.create_image(0, 0, anchor='nw', image=img_tk)
            canvas.image_ref = img_tk

        btn = tk.Button(frame, text="Generate Preview", command=update_preview)
        btn.pack(pady=5)

        update_preview()

        return frame

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
