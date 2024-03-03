from tkinter import *
import cv2
from PIL import Image, ImageTk
import image_detector
from arduino_communication import ArduinoCommunication

#define colors
bg_color = "#121212"
level1_color = "#1e1e1e"
level2_color = "#242424"
level3_color = "#2c2c2c"
level4_color = "#333333"
level5_color = "#383838"
primary_color = "#03DAC6"
secondary_color = "#BB86FC"
tertiary_color = "#AEC6CF"
error_color = "#CF6679"
objects_on_right = True

#define dimensions
width = 700
height = 700

#create main window
main_window = Tk()
#icon = ImageTk.PhotoImage(file="logo.png")
#main_window.wm_iconphoto(False, icon)
main_window.title("Safe-Swing")
main_window.geometry(str(width) + "x" + str(height))
main_window.config(bg=level1_color)
main_window.resizable(height=None, width=None)

#create title frame
title_frame = Frame(main_window, bg=level1_color, width=width, height = 100)
title_frame.grid(row=0, column=0, pady=20)
title_frame.pack_propagate(False)

#create title label
title_label = Label(title_frame,text="Safe-Swing",font=("Satoshi", '30', 'bold'),bg=level1_color,fg=primary_color)
title_label.pack()

#create description label
desc_label = Label(title_frame,text="Save your door and save others!",font=("Satoshi", '12', 'bold italic'),bg=level1_color,fg=tertiary_color)
desc_label.pack()

#create lock label
lock_label = Label(title_frame,text="UNLOCKED",font=("Satoshi", '12', 'bold italic'),bg=level1_color,fg=tertiary_color)
lock_label.pack()

#image vars
webcam = cv2.VideoCapture(0)
detector = image_detector.ObjectDetection()

#arduino door
door = ArduinoCommunication()

#frame for camera
object_view = Label(main_window, bg='blue', width=640, height=480)

#main analysis code
def protect(object_data):
    width_threshold = 0.4 if objects_on_right else 0.6
    should_lock = False
    area_threshold = {"person": 0.2, "car": 0.4, "bicycle": 0.3, "truck": 0.4, "bus": 0.5, "train": 0.5}
    for obj in object_data:
        #Dynamic (tracking) detection

        #Static detection
        if objects_on_right and obj['x2'] > width_threshold or not objects_on_right and obj['x1'] < width_threshold:
            if obj['name'] in area_threshold.keys() and obj['area'] > area_threshold[obj['name']]:
                should_lock = True
                
    if should_lock:
        door.lock_door()
        lock_label.config(text="LOCKED")
        
    else:
        door.unlock_door()
        lock_label.config(text="UNLOCKED")

#arduino door  
def show_feed():
    img_ready, raw_image = webcam.read()
    if img_ready:
        output_data, final_image = detector(raw_image)
        final_image = raw_image
        processed_image = Image.fromarray(final_image)
        processed_image = ImageTk.PhotoImage(processed_image)
        object_view.imgtk = processed_image
        object_view.config(image=processed_image)
        protect(output_data)

    object_view.after(1, show_feed)

object_view.grid(row=1, column=0, pady=20)

#Credits
credits_label = Label(main_window, text="Project for Blueprint 2024 by Sanjay Vijay and Jack Whitman", font=('Satoshi', '10', 'italic'), bg = level1_color, fg = secondary_color, pady=20)
credits_label.grid(row=2, column=0)

show_feed()

#display main window
main_window.mainloop()