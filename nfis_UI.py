from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

resize_factor = 0

#main_screen = Tk()
def click_handler(event):
    print("Mouse position: (%s %s)" % (event.x, event.y))
    return

def update_result():
    global img2
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

'''
path = "example.jpg"
img = ImageTk.PhotoImage(Image.open(path))
image_win = Label(main_screen, image = img)
image_win.bind('<Button>', click_handler)
image_win.pack(side = "top", expand = "yes")
panel = Frame(main_screen)
panel.pack(side = "bottom")
button = Button(panel, text="haha")
button.pack()
mainloop()
'''
path = askopenfilename()
window = Tk()
#path = "example.jpg"
img = Image.open(path)
resize_factor = img.height / 300 if (img.height / 300) > (img.width / 400) else img.width / 400
img = ImageTk.PhotoImage(img.resize((int(img.width/resize_factor), int(img.height/resize_factor))))

image_part = Frame(window)
panel_part = Frame(window)
image_part.pack(side = "top")
panel_part.pack(side = "bottom")

origin_image_frame = LabelFrame(image_part, text="origin image", width = 400, height = 300)
result_image_frame = LabelFrame(image_part, text="result image", width = 400, height = 300)
origin_image_frame.pack(expand = "yes", side = "left")
result_image_frame.pack(expand = "yes", side = "right")
origin_image_frame.pack_propagate(0)
result_image_frame.pack_propagate(0)
origin_image_label = Label(origin_image_frame, image = img)
result_image_label = Label(result_image_frame)
origin_image_label.bind('<Button>', click_handler)
result_image_label.bind('<Button>', click_handler)
origin_image_label.pack(side = "left")
result_image_label.pack(side = "right")

start_button = Button(panel_part, text="open image...", command = open_file)
start_button.pack()
start_button = Button(panel_part, text="start process", command = update_result)
start_button.pack()

mainloop()
