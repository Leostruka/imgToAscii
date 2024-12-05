import sys
from PIL import Image
from tkinter import Tk, filedialog, simpledialog

root = Tk()
root.withdraw()
image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

if not image_path:
    print("No image selected.")
    sys.exit()

scale = simpledialog.askinteger("Input", "Enter scale (e.g., 1 for original size, 2 for half size, 3 for default, etc.):", minvalue=1)
root.destroy()

if not scale or scale < 1:
    scale = 3

img_orig = Image.open(image_path)
w, h = img_orig.width, img_orig.height
image = img_orig.resize((w // scale, h // (scale * 2)))

ascii_pixels = (' ', '.', ':', '-', '=', '+', '*', '#', '%', '@')

max_rgb = max(range(256))
rgb_sub_range = max_rgb / len(ascii_pixels)

def ascii_from_rgb(x, y):
    r, g, b, *rest = image.getpixel((x, y))
    avg_brightness = sum([r, g, b]) / len([r, g, b])

    pixel_index = int(avg_brightness / rgb_sub_range)
    pixel_index = min(max(pixel_index, 0), len(ascii_pixels) - 1)
    ascii_pixel = ascii_pixels[pixel_index]

    return f"{ascii_pixel}" if x < (image.width - 1) \
                else f"{ascii_pixel}\n"

def ascii_art_generator(image):
    return (
        ascii_from_rgb(x, y)
            for y in range(image.height)
            for x in range(image.width)
    )

if __name__ == "__main__":
    ascii_art = ascii_art_generator(image)
    with open('output_cp437.txt', 'w', encoding='cp437') as f:
        for c in ascii_art:
            f.write(c)
