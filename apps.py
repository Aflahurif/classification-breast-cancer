from glob import glob
import tkinter as tk
from tkinter import CENTER, E, W, N,Button, Entry, Frame, Label, StringVar, ttk, filedialog, messagebox, LabelFrame, OptionMenu
from regex import P
from PIL import ImageTk,Image
import fungsi

IMAGE_PATH = 'tmp/breast-cancer-detection.jpg'
WIDTH, HEIGTH = 720, 405

root = tk.Tk()
root.title('Auto')
root.geometry('{}x{}'.format(WIDTH, HEIGTH))

input_accu = StringVar()
input_pred = StringVar()
clicked = StringVar()
clicked.set("benign")
opsi = [
    "benign",
    "malignant"
]
no_img = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((200,200)))
global prediction
global prediction_accu
global panel_ori
global panel_gray
global panel_confus
global tree
global trigger_entry
global data
data = {}
def openNewWindow():
    global newWindow
    newWindow = tk.Toplevel()
    newWindow.title("Accuration")
    newWindow.geometry('1100x500')
    newWindow.grab_set()
    frame_body = Frame(newWindow)
    frame_body.grid(row=0,column=0,pady=20,padx=10, sticky=tk.N)
    frame_div = Frame(frame_body)
    frame_div.grid(row=0,column=0,sticky=N)
    frame_fields = LabelFrame(frame_div, text="Input Image")
    frame_fields.grid(row=0,column=0,sticky=N, padx=15)
    drop = OptionMenu(frame_fields, clicked, *opsi)
    drop.config(width=10)
    drop.grid(row=0,column=1,sticky=W,padx=15)
    lbl_trigger = Label(frame_fields,text='Select Image',font=('bold','12'))
    lbl_trigger.grid(row=0,column=0,sticky=N,padx=15, pady=10)
    trigger_path_button = Button(frame_fields, text='Select', width=30, command=trigger_accuracy)
    trigger_path_button.grid(row=0,column=2, sticky=W, padx=15)

    submit_button = Button(frame_fields, text='Submit', width=12, command=submit_accu)
    submit_button.grid(row=1,column=2,padx=15, sticky=W)
    submit_button = Button(frame_fields, text='Test Ulang', width=12, command=reset_accu)
    submit_button.grid(row=1,column=2,padx=15, pady=10, sticky=E)

    frame_div1 = Frame(frame_body)
    frame_div1.grid(row=0,column=1,sticky=tk.NW,padx=20)
    frame_button = Frame(frame_div1)
    frame_button.grid(row=0,column=0,sticky=N)

    columns = ('File','True','Predict')
    global tree
    tree = ttk.Treeview(frame_button, columns=columns, show='headings', height=5)
    wid = 100

    tree.column('File', anchor=CENTER, stretch=False,width=300)
    tree.heading('File', text='File')
    tree.column('True', anchor=CENTER, stretch=False,width=wid)
    tree.heading('True', text='True')
    tree.column('Predict', anchor=CENTER, stretch=False,width=wid)
    tree.heading('Predict', text='Predict')

    tree.grid(row=0, column=0)

    global panel_confus
    panel_confus = tk.Label(frame_button, image=no_img, width = 320, height = 240)
    panel_confus.grid(row=1,column=0,pady=5)
    lbl_confus = Label(frame_button,text='confusion matrix',font=('bold','12'))
    lbl_confus.grid(row=2,column=0,sticky=N,padx=5)

    global prediction_accu
    prediction_accu = Button(frame_button,text='ACCCURACY', width=10,font=('bold','16'), state='disable')
    prediction_accu.grid(row=3,column=0,sticky='e',pady=10)

def reset_accu():
    global data
    data = {}
    clicked.set("benign")
    for item in tree.get_children():
        tree.delete(item)
    prediction_accu['text'] = 'ACUURACY'
    panel_confus.configure(image=no_img)
    panel_confus.image = no_img

def submit_accu():
    if 'benign' in data.keys() and 'malignant' in data.keys():
        result, img_confus, score = fungsi.get_accuraacy(data)
        for kunci in data.keys():
            for val,rslt in zip(data[kunci],result):
                tree.insert('', tk.END, values=[val,kunci,rslt])
        confus = ImageTk.PhotoImage(Image.open(str(img_confus)).resize((320,240)))
        panel_confus.configure(image=confus)
        panel_confus.image = confus
        prediction_accu['text'] = score

    else:
        messagebox.showerror("error","lengkapi data terlebih dahulu",parent=newWindow)

def NewWindow():
    global newWindow
    newWindow = tk.Toplevel()
    newWindow.title("Prediction")
    newWindow.geometry('1100x500')
    frame_body = Frame(newWindow)
    frame_body.grid(row=0,column=0,pady=20,padx=20, sticky=tk.N)
    frame_div = Frame(frame_body)
    frame_div.grid(row=0,column=0,sticky=E)
    frame_fields = LabelFrame(frame_div, text="Input Image")
    frame_fields.grid(row=0,column=0,sticky=N)

    lbl_trigger = Label(frame_fields,text='Select Image',font=('bold','12'))
    lbl_trigger.grid(row=0,column=0,sticky=N)
    global trigger_entry
    trigger_entry = Entry(frame_fields,textvariable=input_pred,width=40)
    trigger_entry.grid(row=0,column=1,sticky=N)

    trigger_path_button = Button(frame_fields, text='Select', width=12, command=trigger_file)
    trigger_path_button.grid(row=0,column=2,sticky='ns',padx=5)

    submit_button = Button(frame_fields, text='Submit', width=12, command=callback)
    submit_button.grid(row=1,column=1, sticky=E)
    submit_button = Button(frame_fields, text='Reset', width=12, command=reset)
    submit_button.grid(row=1,column=2,pady=15)

    frame_img = LabelFrame(frame_div,text="Image Pre-Processing")
    frame_img.grid(row=1,column=0,sticky=N,pady=(60,5))

    # canvas ori
    global panel_ori
    panel_ori = tk.Label(frame_img, image=no_img, width = 200, height = 200)
    panel_ori.grid(row=0,column=0)
    lbl_ori = Label(frame_img,text='Image Original',font=('bold','12'))
    lbl_ori.grid(row=1,column=0,sticky=N,padx=5)

    # canvas gray
    global panel_gray
    panel_gray = tk.Label(frame_img, image=no_img, width = 200, height = 200)
    panel_gray.grid(row=0,column=1)
    lbl_gray = Label(frame_img,text='Image Grayscale',font=('bold','12'))
    lbl_gray.grid(row=1,column=1,sticky=N,padx=5)

    frame_div1 = Frame(frame_body)
    frame_div1.grid(row=0,column=1,sticky=tk.NW,padx=20)
    frame_button = Frame(frame_div1)
    frame_button.grid(row=0,column=0,sticky=N)

    # define columns
    global tree
    columns = ('degree','energy', 'homogeneity', 'contrast','correlation')
    tree = ttk.Treeview(frame_button, columns=columns, show='headings', height=5)
    wid = 130

    # define headings
    tree.column('degree', anchor=CENTER, stretch=False,width=50)
    tree.heading('degree', text='Degree')
    tree.column('energy', anchor=CENTER, stretch=False,width=wid)
    tree.heading('energy', text='Energy')
    tree.column('homogeneity', anchor=CENTER, stretch=False,width=wid)
    tree.heading('homogeneity', text='Homogeneity')
    tree.column('contrast', anchor=CENTER, stretch=False,width=wid)
    tree.heading('contrast', text='Contrast')
    tree.column('correlation', anchor=CENTER, stretch=False,width=wid)
    tree.heading('correlation', text='Correlation')

    tree.grid(row=0, column=0)

    global prediction
    prediction = Button(frame_button,text='HASIL', width=10,font=('bold','20'), state='disable')
    prediction.grid(row=1,column=0,sticky='e',pady=10)

    newWindow.mainloop()
    return panel_ori
def trigger_file():
    file = filedialog.askopenfilename(initialdir='./tmp/data', title='Choose File Trigger', filetypes=(('png files', '*.png'), ('jpeg files', '*.jpg'), ('all files', '*.*')),parent=newWindow)
    input_pred.set(file)
    
data_tes = {}
def trigger_accuracy():
    file = filedialog.askopenfilenames(initialdir='./tmp/data', title='Choose File Trigger', filetypes=(('png files', '*.png'), ('jpeg files', '*.jpg'), ('all files', '*.*')),parent=newWindow)
    global data
    if file != '':
        data[clicked.get()] = file
        messagebox.showinfo("succes","data "+str(clicked.get())+" berhasil ditambahkan",parent=newWindow)

def callback():
    img = input_pred.get()
    try:
        if img.lower().endswith(('.png', '.jpg', '.jpeg')):
            res,value, pred = fungsi.predict_glcm(img)
            ori = ImageTk.PhotoImage(Image.open(str(res['original'])).resize((200,200)))
            panel_ori.configure(image=ori)
            panel_ori.image = ori
            gray = ImageTk.PhotoImage(Image.open(str(res['gray'])).resize((200,200)))
            panel_gray.configure(image=gray)
            panel_gray.image = gray
            for val in value:
                tree.insert('', tk.END, values=val)
            prediction['text'] = pred
        elif img=='':
            messagebox.showerror("Error","File must fill",parent=newWindow)
            trigger_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error","File must be image",parent=newWindow)
            trigger_entry.delete(0, 'end')
    except:
        messagebox.showerror("Error","File must be image",parent=newWindow)
        trigger_entry.delete(0, 'end')

def reset():
    prediction['text'] = "HASIL"
    panel_ori.configure(image=no_img)
    panel_ori.image = no_img
    panel_gray.configure(image=no_img)
    panel_gray.image = no_img
    for item in tree.get_children():
        tree.delete(item)
    trigger_entry.delete(0, 'end')

# Show image using label
img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).crop((100,0,900,450)).resize((WIDTH, HEIGTH)))
canvas = tk.Canvas(root, width=WIDTH, height=HEIGTH)
canvas.pack()

canvas.background = img  # Keep a reference in case this code is put in a function.
bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

label_msg = canvas.create_text((350, 40), text="Cancer Breast Classification\nWith SVM Method", font="MSGothic 20 bold", fill="#652828", justify="center")

button1 = tk.Button(root, text="Accuration", width=12,font=('bold','12'),command = openNewWindow)
button_window1 = canvas.create_window(580, 150, anchor=tk.NW, window=button1)
button2 = tk.Button(root, text="Prediction", width=12,font=('bold','12'),command = NewWindow)
button_window2 = canvas.create_window(580, 200, anchor=tk.NW, window=button2)


root.mainloop()
