import tkinter as tk
from tkinter import PhotoImage

def insert_number(number):
    text_box.insert(tk.END, number)

def backspace():
    current_text = text_box.get("1.0", tk.END)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, current_text[:-2])

def show_dial_interface():
    entered_number = text_box.get("1.0", tk.END).strip()
    
    dial_window = tk.Toplevel(r)
    dial_window.title("Dialing...")
    dial_window.geometry("300x200")

    number_label = tk.Label(dial_window, text=f"Dialing: {entered_number}", font=("Arial", 18))
    number_label.pack(pady=20)

    # Load and display the image
    try:
        img = PhotoImage(file="dialing_interface.png")  # Replace with the path to your image file
        image_label = tk.Label(dial_window, image=img)
        image_label.image = img  # Keep a reference to the image to prevent garbage collection
        image_label.pack(pady=20)
    except Exception as e:
        placeholder_label = tk.Label(dial_window, text="Image not found", font=("Arial", 14))
        placeholder_label.pack(pady=20)

    close_button = tk.Button(dial_window, text="Close", command=dial_window.destroy)
    close_button.pack(pady=10)

r = tk.Tk()
r.title('GameZone')
r.geometry("500x400")

label = tk.Label(r, text="mobile phone ", font=("Areal", 18))
label.pack(padx=20, pady=20)

text_box = tk.Text(r, height=3, font=('areal', 16))
text_box.pack(padx=10, pady=10)

buttonframe = tk.Frame(r)
buttonframe.pack(fill="x", padx=10, pady=10)

buttons = [
    ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
    ("*", 3, 0), ("0", 3, 1), ("#", 3, 2),
    ("Dial", 4, 0)
]

for (text, row, col) in buttons:
    button = tk.Button(buttonframe, text=text, font=('Arial', 18), command=lambda t=text: insert_number(t))
    button.grid(row=row, column=col, sticky="ew")

space_button = tk.Button(buttonframe, text="space", font=('Arial', 18), command=lambda: insert_number(" "))
space_button.grid(row=4, column=1, columnspan=2, sticky="ew")

backspace_button = tk.Button(buttonframe, text="Delete", font=('Arial', 18), command=backspace)
backspace_button.grid(row=4, column=2, sticky="ew")

dial_button = tk.Button(buttonframe, text="Dial", font=('Arial', 18), command=show_dial_interface)
dial_button.grid(row=5, column=0, columnspan=3, sticky="ew")

buttonframe.columnconfigure([0, 1, 2], weight=1)

r.mainloop()
