from tkinter import *
import cv2
from PIL import Image, ImageTk

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

#define dimensions
width = 500
height = 500

#create main window
main_window = Tk()
icon = ImageTk.PhotoImage(file="logo.png")
main_window.wm_iconphoto(False, icon)
main_window.title("Safe-Swing")
main_window.geometry(str(width) + "x" + str(height))
main_window.config(bg=level1_color)
main_window.resizable(height=None, width=None)

#create title frame
title_frame = Frame(main_window, bg=level1_color, width=width, height = 100)
title_frame.grid(row=0, column=0, pady=20)
title_frame.pack_propagate(False)

#create title label
title_label = Label(title_frame,text="Nutrireader",font=("Satoshi", '30', 'bold'),bg=level1_color,fg=primary_color)
title_label.pack()

#create description label
desc_label = Label(title_frame,text="Nutrition with Nutrireader makes you the leader!",font=("Satoshi", '12', 'bold italic'),bg=level1_color,fg=tertiary_color)
desc_label.pack()

#create frames, labels, and entries for ingredients
data_frame = Frame(main_window, bg=level1_color)
data_frame.grid(row=1, column=0)

#radio buttons for type of item
item_type = IntVar()
food_option_frame = Frame(data_frame, bg=level1_color)
food_option_frame.grid(row = 7, column=0, columnspan=3)
type_label = Label(food_option_frame, font=("Satoshi", 10), text="Item Type: ", fg = 'white', bg=level1_color)
type_label.grid(row=0,column=0,sticky="E")
food_button = Radiobutton(food_option_frame, text = "Food", variable=item_type, value = 0, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
food_button.grid(row=0,column=1)
drink_button = Radiobutton(food_option_frame, text = "Drink", variable=item_type, value = 1, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
drink_button.grid(row=0,column=2)

#radio buttons for verboseness
explanation_type = IntVar()
ex_option_frame = Frame(data_frame, bg=level1_color)
ex_option_frame.grid(row = 8, column=0, columnspan=3)
ex_label = Label(ex_option_frame, font=("Satoshi", 10), text="Explanation Length: ", bg=level1_color, fg = 'white')
ex_label.grid(row=0,column=0,sticky="E")
short_button = Radiobutton(ex_option_frame, text = "Short", variable=explanation_type, value = 0, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
short_button.grid(row=0,column=1)
med_button = Radiobutton(ex_option_frame, text = "Medium", variable=explanation_type, value = 1, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
med_button.grid(row=0,column=2)
long_button = Radiobutton(ex_option_frame, text = "Long", variable=explanation_type, value = 2, font = ("Satoshi", 10), fg=tertiary_color, bg=level1_color, activeforeground=primary_color, activebackground=level1_color, selectcolor=level1_color)
long_button.grid(row=0,column=3)

#image vars
webcam = cv2.VideoCapture(0)

#open camera function
def open_cam():
    #show frames of camera
    def show_frames():
        result, raw_image = webcam.read()
        if result:
            converted_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)
            selected_image = Image.fromarray(converted_image)
            final_image = ImageTk.PhotoImage(selected_image)
            display_frame.imgtk = final_image
            display_frame.config(image=final_image)

        #animate frame
        display_frame.after(10, show_frames)
    #initialize frame
    cam_window = Toplevel(main_window)
    cam_window.config(bg=level1_color)
    cam_window.wm_iconphoto(False, icon)
    display_frame = Label(cam_window)
    display_frame.pack()
    capture_button = Button(cam_window, font=('Satoshi', '12', 'normal'), text="Capture", bg=level4_color, fg=error_color, activebackground=level4_color, activeforeground=primary_color, width=50, command=capture)
    capture_button.pack()
    show_frames()
    cam_window.mainloop()

#Camera button
submit_button = Button(data_frame, font=('Satoshi', '12', 'normal'), text="Open Camera for Scanning", bg=level4_color, fg=tertiary_color, activebackground=level4_color, activeforeground=primary_color, width=50, command=open_cam)
submit_button.grid(row=10, column=0, columnspan=3)

#Credits
credits_label = Label(main_window, text="Project for Blueprint 2024 by Sanjay Vijay and Jack Whitman", font=('Satoshi', '10', 'italic'), bg = level1_color, fg = secondary_color, pady=20)
credits_label.grid(row=2, column=0)

#display main window
main_window.mainloop()