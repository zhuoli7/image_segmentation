from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import test_504

clicked_list = []

window_width = 1000

class input_item(Frame):
    def __init__(self, title_str, m_width, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.title = Label(self, text = title_str)
        self.title.pack(side = 'left')
        self.input_box = Entry(self, bd = 5, width = m_width)
        self.input_box.pack(side = 'right')

    def get_text(self):
        return self.input_box.get()
    
    def insert(self, default_text):
        self.input_box.insert(END, default_text)


def click_handler(event):# this is the handler of the mouse clicking
    print("Mouse position: (%s %s)" % (event.x, event.y))
    global origin_image_label
    clicked_list.append([event.x, event.y])
    origin_image_label.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width = 2, fill = 'red', outline = 'red')
    return

def update_result():# this is the handler of the start processing button
    global sample_rate_input
    global penalty_input
    global img2
    global clicked_list
    global path #the name of the input image
    global sample_rate
    global penalty
    global clusters_input

    sample_rate = int(sample_rate_input.get_text())#sampling rate
    penalty = float(penalty_input.get_text())   #penalty set
    clusters = int(clusters_input.get_text())
    #the default value is 4 for sample_rate, 0.02 for penalty.

    
    #the name of the input image is stored in path, use it.
    #----------------put your code here------------------#
    test_504.proc(path, path, sample_rate, penalty, clusters)
    #----------------------------------------------------#
    img2 = Image.open('result.jpg')
    resize_factor = img2.height / 300 if (img2.height / 300) > (img2.width / (window_width / 2)) else img2.width / (window_width / 2)
    img2 = ImageTk.PhotoImage(img2.resize((int(img2.width /resize_factor), int(img2.height /resize_factor))))
    result_image_label.configure(image = img2)
    return

def open_file():
    global img
    global clicked_list
    global path

    clicked_list = []
    path = input_image_name.get_text()
    img = Image.open(path)
    resize_factor = img.height / 300 if (img.height / 300) > (img.width / (window_width / 2)) else img.width / (window_width / 2)
    img = ImageTk.PhotoImage(img.resize((int(img.width/resize_factor), int(img.height/resize_factor))))
    origin_image_label.create_image(0, 0, anchor=NW, image = img)

flag = 1
window = Tk()
window.title('nfis')

image_part = Frame(window)
panel_part = LabelFrame(window, text="panel", width = window_width, height = 70)
panel_part.pack_propagate(0)
image_part.pack(side = "top")
panel_part.pack(side = "bottom")

origin_image_frame = LabelFrame(image_part, text="origin image", width = window_width / 2, height = 300)
result_image_frame = LabelFrame(image_part, text="result image", width = window_width / 2, height = 300)
origin_image_frame.pack(expand = "yes", side = "left")
result_image_frame.pack(expand = "yes", side = "right")
origin_image_frame.pack_propagate(0)
result_image_frame.pack_propagate(0)
origin_image_label = Canvas(origin_image_frame, width = window_width / 2, height = 300)
result_image_label = Label(result_image_frame)
origin_image_label.pack_propagate(0)
origin_image_label.bind('<Button>', click_handler)
result_image_label.bind('<Button>', click_handler)
origin_image_label.pack(side = "left")
result_image_label.pack(side = "top")

input_image_name = input_item('input', int(window_width / 70), panel_part)
input_image_name.insert('cow.jpg')
input_image_name.pack(side = "left")

open_button = Button(panel_part, text="open", command = open_file)
open_button.pack(side = "left", padx=10)

sample_rate_input = input_item('sample rate', int(window_width / 70), panel_part)
sample_rate_input.insert('4')   # change the default value for sample rate if you want
sample_rate_input.pack(side = "left", padx=10)

clusters_input = input_item('clusters', int(window_width / 70), panel_part)
clusters_input.insert('2')   # change the default value for sample rate if you want
clusters_input.pack(side = "left", padx=10)

penalty_input = input_item('penalty', int(window_width / 70), panel_part)
penalty_input.insert('0.02')    # change the default value for penalty if you want
penalty_input.pack(side = "left", padx=10)

start_button = Button(panel_part, text="start processing", command = update_result)
start_button.pack(side = "right", padx=10)

window.mainloop()