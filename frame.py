from tkinter import *
import cv2
from PIL import Image, ImageTk
import image_detector
from arduino_communication import ArduinoCommunication
import numpy as np

#define colors
bg_color = "#00008b"
level1_color = "#00003b"
level2_color = "#008b8b"
level3_color = "#2c2c2c"
level4_color = "#343333"
level5_color = "#383838"
primary_color = "#03DAC6"
secondary_color = "#BB86FC"
tertiary_color = "#AEC6CF"
error_color = "#CF6679"
objects_on_right = True

#define dimensions
width = 700
height = 750

#create main window
main_window = Tk()
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


#helper functions for analysis
def is_living(name):
        if name == 'person' or name == 'bicycle':
            return True
        return False

def distance_between(obj1, obj2):
    return np.sqrt( abs( (obj1['x1'] + obj1['x2'])/2 - (obj2['x1'] + obj2['x2'])/2 )**2 + abs( (obj1['y1'] + obj1['y2'])/2 - (obj2['y1'] + obj2['y2'])/2 )**2 )


#main analysis code
def protect(object_data):
    #dynamic detection variables
    size_change_new_threshold = 3.0
    position_change_new_threshold = 0.75
    dA_dt_lock_threshold = 1.1
    current_largest_object = {'x1':0, 'x2':1, 'y1':0, 'y2':1, 'area': 0.0}

    #static detection variables
    width_threshold = 0.4 if objects_on_right else 0.6
    area_thresholds = {"person": 0.2, "car": 0.4, "bicycle": 0.3, "truck": 0.4, "bus": 0.5, "train": 0.5}

    should_lock = False

    #Get the largest object in this frame
    for obj in object_data:
        if is_living(obj['name']) and (not current_largest_object or obj['area'] > current_largest_object['area']):
            current_largest_object = obj

    if not detector.get_prev_obj():
            detector.set_prev_obj(current_largest_object)

    #If the largest object has changed according to thresholds, set it to the new object
    if current_largest_object['area']/(1 if not detector.get_prev_obj()['area'] else detector.get_prev_obj()['area'])  > size_change_new_threshold or distance_between(current_largest_object, detector.get_prev_obj()) > position_change_new_threshold:
        detector.set_prev_obj(current_largest_object)
    
    #If dA/dt is sufficiently high, lock the door
    elif current_largest_object['area']/(1 if not detector.get_prev_obj()['area'] else detector.get_prev_obj()['area']) > dA_dt_lock_threshold:
        should_lock = True
    
    for obj in object_data:
        #Static detection
        if objects_on_right and obj['x2'] > width_threshold or not objects_on_right and obj['x1'] < width_threshold:
            if obj['name'] in area_thresholds.keys() and obj['area'] > area_thresholds[obj['name']]:
                should_lock = True
    
    detector.set_prev_obj(current_largest_object)
    
    #Lock or unlock the door     
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