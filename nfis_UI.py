from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
from pathlib import Path

class input_item(Frame):
    def __init__(self, title_str, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.title = Label(self, text = title_str)
        self.title.pack(side = 'left')
        self.input_box = Entry(self, bd = 5)
        self.input_box.pack(side = 'right')

    def get_text(self):
        return self.input_box.get()
    
    def insert(self, default_text):
        self.input_box.insert(END, default_text)

resize_factor = 0

def click_handler(event):# this is the handler of the mouse clicking
    print("Mouse position: (%s %s)" % (event.x, event.y))
    global origin_image_label
    origin_image_label.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, width = 2, fill = 'red', outline = 'red')
    global sample_rate_input
    global penalty_input
    sample_rate = float(sample_rate_input.get_text())#sampling rate
    penalty = float(penalty_input.get_text())   #penalty set
    #the default value is 4 for sample_rate, 0.02 for penalty.

    #----------------put your code here------------------#


    #----------------------------------------------------#
    return

def update_result():
    global img2
    global path2
    img2 = Image.open(path2)
    img2 = ImageTk.PhotoImage(img2.resize((int(img2.width/resize_factor), int(img2.height/resize_factor))))
    result_image_label.configure(image = img2)
    return

def open_file():
    path = askopenfilename()
    img = Image.open(path)
    resize_factor = img.height / 300 if (img.height / 300) > (img.width / 400) else img.width / 400
    img = ImageTk.PhotoImage(img.resize((int(img.width/resize_factor), int(img.height/resize_factor))))
    origin_image_label.configure(image = img)



foreground_list = []
#path = askopenfilename(filetypes=[("Image File",'.jpg')])
#path = Path(path)
window = Tk()
window.title('nfis')
path = "example.jpg"  # change this line to the name of input image
path = "result.jpg"   # change this line to the name of output image
img = Image.open(path)
resize_factor = img.height / 300 if (img.height / 300) > (img.width / 400) else img.width / 400
img = ImageTk.PhotoImage(img.resize((int(img.width/resize_factor), int(img.height/resize_factor))))
image_part = Frame(window)
panel_part = LabelFrame(window, text="panel", width = 800, height = 70)
panel_part.pack_propagate(0)
image_part.pack(side = "top")
panel_part.pack(side = "bottom")

origin_image_frame = LabelFrame(image_part, text="origin image", width = 400, height = 300)
result_image_frame = LabelFrame(image_part, text="result image", width = 400, height = 300)
origin_image_frame.pack(expand = "yes", side = "left")
result_image_frame.pack(expand = "yes", side = "right")
origin_image_frame.pack_propagate(0)
result_image_frame.pack_propagate(0)
origin_image_label = Canvas(origin_image_frame)
origin_image_label.pack_propagate(0)
origin_image_label.create_image(0, 0, anchor=NW, image = img)
result_image_label = Label(result_image_frame)
origin_image_label.bind('<Button>', click_handler)
result_image_label.bind('<Button>', click_handler)
origin_image_label.pack(side = "left")
result_image_label.pack(side = "right")

sample_rate_input = input_item('sample rate', panel_part)
sample_rate_input.insert('4')   # change the default value for sample rate if you want
sample_rate_input.pack(side = "left", padx=10)

penalty_input = input_item('penalty', panel_part)
penalty_input.insert('0.02')    # change the default value for penalty if you want
penalty_input.pack(side = "left", padx=10)

start_button = Button(panel_part, text="start processing", command = update_result)
start_button.pack(side = "right", padx=10)

mainloop()
