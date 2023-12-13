import os
from PIL import Image as PILImage, ImageFilter
import numpy as np
from threading import Thread
from tkinter import *

# Функция применения фильтра "sharpen"
def apply_sharpen_filter(image):
    return image.filter(ImageFilter.SHARPEN)

# Функция применения фильтра "sepia"
def apply_sepia_filter(image):
    img_array = np.array(image)
    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                            [0.349, 0.686, 0.168],
                            [0.272, 0.534, 0.131]])
    sepia_image = np.dot(img_array, sepia_matrix.T).clip(0, 255).astype(np.uint8)
    return PILImage.fromarray(sepia_image)

# Функция применения фильтра "resize"
def apply_resize_filter(image, size=(400, 100)):
    return image.resize(size)

def apply_filter(input_path, output_folder, filter_name):
    image = PILImage.open(input_path)
    filtered_image = None

    if filter_name == 'sharpen':
        filtered_image = apply_sharpen_filter(image)
    elif filter_name == 'sepia':
        filtered_image = apply_sepia_filter(image)
    elif filter_name == 'resize':
        filtered_image = apply_resize_filter(image)

    if filtered_image:
        filename, ext = os.path.splitext(os.path.basename(input_path))
        output_path = os.path.join(output_folder, f"{filename}_{filter_name}{ext}")
        filtered_image.save(output_path)

def process_image(input_path, output_folder, filters):
    for filter_name in filters:
        apply_filter(input_path, output_folder, filter_name)

def process_images(input_folder, output_folder, filters):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [filename for filename in os.listdir(input_folder) if
                   filename.lower().endswith((".jpg", ".jpeg", ".png"))]

    threads = []

    for filename in image_files:
        input_path = os.path.join(input_folder, filename)
        thread = Thread(target=process_image, args=(input_path, output_folder, filters))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def apply_filters():
    filters = []
    if var_sharpen.get():
        filters.append("sharpen")
    if var_sepia.get():
        filters.append("sepia")
    if var_resize.get():
        filters.append("resize")

    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()

    if filters and input_folder and output_folder:
        process_images(input_folder, output_folder, filters)
        result_label.config(text="Обработка завершена.")
    else:
        result_label.config(text="Выберите фильтры и укажите папки.")


window = Tk()
window.title("Программа для обработки изображений")

Label(window, text="Папка входных изображений:").grid(row=0, column=0)
input_folder_entry = Entry(window)
input_folder_entry.grid(row=0, column=1)
Label(window, text="Папка выходных изображений:").grid(row=1, column=0)
output_folder_entry = Entry(window)
output_folder_entry.grid(row=1, column=1)

var_sharpen = IntVar()
sharpen_checkbox = Checkbutton(window, text="Sharpen", variable=var_sharpen)
sharpen_checkbox.grid(row=2, column=0)
var_sepia = IntVar()
sepia_checkbox = Checkbutton(window, text="Sepia", variable=var_sepia)
sepia_checkbox.grid(row=2, column=1)
var_resize = IntVar()
resize_checkbox = Checkbutton(window, text="Resize", variable=var_resize)
resize_checkbox.grid(row=2, column=2)

process_button = Button(window, text="Обработать", command=apply_filters)
process_button.grid(row=3, column=1)

result_label = Label(window, text="")
result_label.grid(row=4, column=0, columnspan=3)

window.mainloop()
