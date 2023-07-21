import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def find_gif_files():
    directory = filedialog.askdirectory()
    if directory:
        found_files.clear()
        for filename in os.listdir(directory):
            if filename.endswith('.gif'):
                gif_path = os.path.join(directory, filename)
                found_files.append(gif_path)
        found_var.set('\n'.join(found_files))
        found_text.delete(1.0, tk.END)
        found_text.insert(tk.END, found_var.get())

def convert_files():
    for gif_path in found_files:
        mp4_path = gif_path.replace('.gif', '.mp4')
        convert_gif_to_mp4(gif_path, mp4_path)

def convert_gif_to_mp4(gif_path, mp4_path):
    command = [
        'ffmpeg',
        '-ss', '0',
        '-i', gif_path,
        '-movflags', 'faststart',
        '-pix_fmt', 'yuv420p',
        '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
        mp4_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Conversion of {gif_path} succesful.")
        converted_files.append(mp4_path)
        converted_var.set('\n'.join(converted_files))
        converted_text.delete(1.0, tk.END)  # clear content
        converted_text.insert(tk.END, converted_var.get())
    except subprocess.CalledProcessError as e:
        print(f"error converting {gif_path} to MP4:", e)

root = tk.Tk()

found_files = []
converted_files = []

find_button = tk.Button(root, text="Select Directory GIF", command=find_gif_files)
find_button.pack()

convert_button = tk.Button(root, text="Convert to MP4", command=convert_files)
convert_button.pack()

found_label = tk.Label(root, text="Found Files:")
found_label.pack()

found_var = tk.StringVar()
found_text = tk.Text(root, height=10, width=40)
found_text.pack()

found_scrollbar = tk.Scrollbar(root, command=found_text.yview)
found_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

found_text['yscrollcommand'] = found_scrollbar.set

converted_label = tk.Label(root, text="Converted Files:")
converted_label.pack()

converted_var = tk.StringVar()
converted_text = tk.Text(root, height=10, width=40)
converted_text.pack()

converted_scrollbar = tk.Scrollbar(root, command=converted_text.yview)
converted_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

converted_text['yscrollcommand'] = converted_scrollbar.set

root.mainloop()
