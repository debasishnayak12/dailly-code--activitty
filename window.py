import cv2
import os
import sys
import tkinter as tk
from tkinter import Button, Label, Entry, messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime
import threading
from add_client import send_data
from update_api import update_filename

default_folder = "C:\\PhotoBook"

# Get absolute path to resource, works for dev and for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

frame_png = resource_path("frame.png")
icon_image = resource_path("icon.ico")

cam = cv2.VideoCapture(0)
captured_frame = None
running = True  # Flag to control frame updating

# Create window
window = tk.Tk()
window.title("Capture image")
window.iconbitmap(icon_image)
window.minsize(1000, 600)

# main_frame = tk.Frame(window)
# main_frame.pack(expand=True, fill='none', padx=20, pady=20)

# video_frame = tk.Frame(main_frame)
# video_frame.pack(side='top', fill='both', expand=True)


video_label = ttk.Label(window)
video_label.pack()

# Create frames for organization
main_frame = tk.Frame(window)
main_frame.pack(expand=True, fill='none', padx=20, pady=20)

video_frame = tk.Frame(main_frame)
video_frame.pack(side='top', fill='both', expand=True)

# Create directory entry label
directory_label = Label(main_frame, text="Save To :")
directory_entry = Entry(main_frame, width=70)
directory_entry.insert(0, default_folder)

dots=0



def create_details_window():
    global captured_frame
    global details_frame, name_entry, email_entry, phone_entry

    details_frame = tk.Frame(main_frame, padx=20, pady=20, bg="#f0f0f0")  # Light gray background
    details_frame.pack(expand=True, fill='none')

    name_label = Label(details_frame, text="User_name :", bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
    name_label.pack(anchor="center", pady=10)
    name_entry = Entry(details_frame, width=40)
    name_entry.pack(pady=5)

    email_label = Label(details_frame, text="e-mail :", bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
    email_label.pack(anchor="center", padx=50, pady=5)
    email_entry = Entry(details_frame, width=40)
    email_entry.pack(padx=50, pady=5)

    phone_label = Label(details_frame, text="Phone :", bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
    phone_label.pack(anchor="center", pady=5)
    phone_entry = Entry(details_frame, width=40)
    phone_entry.pack(pady=5)

    tk.Button(details_frame, text="Submit", command=submit_details, bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=10)
    start_button.pack_forget()

def submit_details():
    print("captured_frame :", captured_frame)
    Name = name_entry.get()
    email = email_entry.get()
    Mobile = phone_entry.get()

    if Name and email and Mobile:
        data = send_data(Name, email, Mobile)
        result = data.json()
        if isinstance(result, dict) and 'id' in result:
            global id
            id = result['id']
            print("This is id :", id)

            details_frame.pack_forget()
            update_frame()

        else:
            messagebox.showerror("Error", "Failed to retrieve id from server")
    else:
        messagebox.showerror("Input Error", "Please fill in all fields")

def update_frame():
    global running
    if not running:
        return

    global captured_frame
    ret, frame = cam.read()
    if ret:
        fliped_frame = cv2.flip(frame, 1)  # Flipped frame left to right
        frame_rgb = cv2.cvtColor(fliped_frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame_rgb.shape
        aspect_ratio = w / h

        new_width = 500
        new_height = int(new_width / aspect_ratio)

        if new_height > 500:
            new_height = 500
            new_width = int(new_height * aspect_ratio)

        resized_frame = cv2.resize(frame_rgb, (new_width, new_height))
        blank_frame = Image.new("RGB", (500, 500), (0, 0, 0))
        resized_pil = Image.fromarray(resized_frame)

        x = (500 - new_width) // 2
        y = (500 - new_height) // 2
        blank_frame.paste(resized_pil, (x, y))
        frame_image = Image.open(frame_png).convert("RGBA")
        frame_image = frame_image.resize((500, 500), Image.LANCZOS)

        combined_image = Image.alpha_composite(blank_frame.convert("RGBA"), frame_image)
        imageTk = ImageTk.PhotoImage(image=combined_image)
        video_label.imageTk = imageTk
        video_label.configure(image=imageTk)
        video_label.pack(side="top",padx=0,pady=0)
        capture_button.pack(side="left", padx=10)
        start_button.pack_forget()
    window.after(10, update_frame)

def capture_image():
    global captured_frame,running
    running=False
    ret, frame = cam.read()
    if ret:
        fliped_frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(fliped_frame, cv2.COLOR_BGR2RGB)
        h, w, _ = cv2image.shape
        crop_size = 500
        start_x = max(0, (w - crop_size) // 2)

        if h < crop_size:
            padding = (crop_size - h) // 2
            cv2image = cv2.copyMakeBorder(cv2image, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            h = crop_size

        start_y = max(0, (h - crop_size) // 2)
        cropped_frame = cv2image[start_y:start_y + crop_size, start_x:start_x + crop_size]

        img = Image.fromarray(cropped_frame).convert("RGBA")
        captured_frame = cropped_frame

        frame_image = Image.open(frame_png).convert("RGBA")
        frame_image = frame_image.resize((crop_size, crop_size), Image.LANCZOS)

        if img.size == frame_image.size:
            combined_image = Image.alpha_composite(img, frame_image)
            imagetk = ImageTk.PhotoImage(image=combined_image)
            video_label.imagetk = imagetk
            video_label.configure(image=imagetk)

            start_button.pack_forget()
            capture_button.pack_forget()
            retake_button.pack(side='left', padx=10)
            submit_button.pack(side='left', padx=10)
            directory_label.pack(pady=5)
            directory_entry.pack(pady=5)
        else:
            print("Size of cropped image and frame image do not match")
    else:
        print("Failed to capture image")

# def start_again():
#     global running,cam
#     running = True
#     cam = cv2.VideoCapture(0)  # Reinitialize the camera
#     # Restart the frame update loop
#     # main_frame = tk.Frame(window)
#     # main_frame.pack(expand=True, fill='none', padx=20, pady=20)
    
#     video_label.pack_forget()
#     start_button.pack()

def show_success_message():
    success_window = tk.Toplevel(window)
    success_window.title("Success message :")
    success_window.geometry("200x100")

    label = tk.Label(success_window, text="Saved Successfully !", pady=20)
    label.pack()

    window.after(3000, success_window.destroy)
def start_again():
    global running, cam
    running = True
    #cam = cv2.VideoCapture(0)  # Reinitialize the camera
    
    # Reset layout
    start_button.pack(anchor="center", expand=True, padx=20, pady=20)
    
    # Ensure other widgets are in the correct place
    directory_label.pack_forget()
    directory_entry.pack_forget()
    submit_button.pack_forget()
    retake_button.pack_forget()

    # Optionally, clear any additional widgets if needed

    # video_label = ttk.Label(window)
    # video_label.pack(side="top",padx=0,pady=0)

    # # Create frames for organization
    # main_frame = tk.Frame(window)
    # main_frame.pack(expand=True, fill='none', padx=20, pady=0)


    # # Create directory entry label
    # directory_label = Label(main_frame, text="Save To :")
    # directory_entry = Entry(main_frame, width=70)
    # directory_entry.insert(0, default_folder)
    
    #start_button.pack(anchor="center", expand=True, padx=20, pady=20)
   
    


# loader_frame = tk.Frame(window, bg="#ffffff")
# loader_label = tk.Label(loader_frame, text="Loading...", font=("Helvetica", 16), bg="#ffffff")
# loader_label.pack(padx=20, pady=20)



# def show_loader():
#     global loading_label
#     loading_label = tk.Label(window, text="Loading", font=("Helvetica", 16))
#     loading_label.pack(anchor="center", expand=True, padx=20, pady=20)
#     update_loading_text()

# def update_loading_text():
#     global dots
    
#     loading_label.config(text="Loading" + "." * dots)
#     dots = (dots + 1) % 4  # Cycle through 0, 1, 2, 3 dots
#     window.after(500, update_loading_text)  # Update every 500 ms

# def hide_loading():
#     global loading_label
#     loading_label.pack_forget()
    


def submit_image():
    global id, captured_frame, running
    if captured_frame is not None:
        folder_to_save = directory_entry.get()
        if not os.path.exists(folder_to_save):
            messagebox.showerror("Error", f"Can't find the directory : {folder_to_save}")
            return

        cv2image = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image).convert("RGBA")
        frame_image = Image.open(frame_png).convert("RGBA")
        frame_image = frame_image.resize((500, 500), Image.LANCZOS)

        combined_image = Image.alpha_composite(img, frame_image)

        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"{timestamp}.png"
        filepath = os.path.join(folder_to_save, filename)
        combined_image.save(filepath)
        print(f"Image saved {filepath}")
        print("last_row_id:", id)

        update_filename(id, filename)

        captured_frame = None
        submit_button.pack_forget()
        retake_button.pack_forget()
        start_button.pack_forget()
        capture_button.pack_forget()
        directory_label.pack_forget()
        directory_entry.pack_forget()
        video_label.pack_forget()
        #cam.release()

        # Show loader while waiting for the start button
        show_success_message()

        threading.Thread(target=start_again,daemon=True).start()

def retake_image():
    global captured_frame,running
    running=True
    captured_frame = None
    update_frame()
    submit_button.pack_forget()
    # start_button.pack_forget()
    retake_button.pack_forget()
    # video_label.pack()
    capture_button.pack(side='left', padx=10)

button_frame = tk.Frame(window)
button_frame.pack(side='bottom', pady=10)


start_button = Button(main_frame, text="Start", command=create_details_window, relief="raised", bg="#78f88e", width=15, height=2, font=("Helvetica", 16))
start_button.pack(anchor="center", expand=True, padx=20, pady=20)

capture_button = Button(button_frame, text="Click to Capture", command=capture_image, relief="raised", bg="#fdf53b")

submit_button = Button(button_frame, text="Save", command=submit_image, relief="raised", bg="#67ecfd")

retake_button = Button(button_frame, text="Retake", command=retake_image, relief="raised", bg="#78f88e")

window.mainloop()

cam.release()
cv2.destroyAllWindows()
