from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def reduce_image_size(input_path, output_dir, max_size=1000000, max_iterations=10):
    if os.path.getsize(input_path) <= max_size:
        messagebox.showinfo("Información", f"La imagen {input_path} ya está por debajo del tamaño máximo permitido.")
        return
    
    _, extension = os.path.splitext(input_path)
    if extension.lower() == ".png":
        process_png(input_path, output_dir, max_size, max_iterations)
    elif extension.lower() in [".jpg", ".jpeg"]:
        process_jpg(input_path, output_dir, max_size, max_iterations)
    else:
        messagebox.showerror("Error", "El formato de archivo no es compatible.")

def process_png(input_path, output_dir, max_size, max_iterations):
    img = Image.open(input_path)

    filename = os.path.basename(input_path)
    filename_no_extension, _ = os.path.splitext(filename)
    output_path = os.path.join(output_dir, filename_no_extension + '_reducida.png')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    iterations = 0
    while os.path.getsize(output_path) > max_size and iterations < max_iterations:
        width, height = img.size
        img = img.resize((width - int(width * 0.1), height - int(height * 0.1)), Image.LANCZOS)
        img.save(output_path, optimize=True)
        iterations += 1

    messagebox.showinfo("Información", f"La imagen se ha guardado en {output_path}, tamaño: {os.path.getsize(output_path)} bytes.")

def process_jpg(input_path, output_dir, max_size, max_iterations):
    img = Image.open(input_path)

    filename = os.path.basename(input_path)
    filename_no_extension, _ = os.path.splitext(filename)
    output_path = os.path.join(output_dir, filename_no_extension + '_reducida.jpg')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    iterations = 0
    while iterations < max_iterations:
        width, height = img.size
        img = img.resize((width - int(width * 0.1), height - int(height * 0.1)), Image.LANCZOS)
        img.save(output_path, optimize=True)
        iterations += 1

        if os.path.getsize(output_path) <= max_size:
            break

    messagebox.showinfo("Información", f"La imagen se ha guardado en {output_path}, tamaño: {os.path.getsize(output_path)} bytes.")

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        input_path.set(file_path)

def select_output_dir():
    directory = filedialog.askdirectory()
    if directory:
        output_dir.set(directory)

def start_process():
    if input_path.get() and output_dir.get():
        reduce_image_size(input_path.get(), output_dir.get())
    else:
        messagebox.showwarning("Advertencia", "Debe seleccionar una imagen y un directorio de salida.")

# Configuracion de la interfaz grafica
root = tk.Tk()
root.title("Reductor de Tamaño de Imágenes")

input_path = tk.StringVar()
output_dir = tk.StringVar()

tk.Label(root, text="Ruta de la imagen:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=input_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Seleccionar imagen", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Directorio de salida:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=output_dir, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Seleccionar directorio", command=select_output_dir).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Iniciar proceso", command=start_process).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
