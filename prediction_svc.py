import tkinter as tk
from tkinter import CENTER, E, W, N,Button, Entry, Frame, Label, StringVar, ttk, filedialog, messagebox, LabelFrame
from regex import P
from PIL import ImageTk,Image
import fungsi

def trigger_file():
    file = filedialog.askopenfilename(initialdir='./', title='Choose File Trigger', filetypes=(('png files', '*.png'), ('jpeg files', '*.jpg'), ('all files', '*.*')))
    trigger.set(file)
    # print(file)

root = tk.Tk()
root.title('Auto')
root.geometry('1100x500')
frame_body = Frame(root)
frame_body.grid(row=0,column=0,pady=20,padx=20, sticky=tk.N)
frame_div = Frame(frame_body)
frame_div.grid(row=0,column=0,sticky=E)
frame_fields = LabelFrame(frame_div, text="Input Image")
frame_fields.grid(row=0,column=0,sticky=N)

def callback():
    img = trigger.get()
    if img.lower().endswith(('.png', '.jpg', '.jpeg')):
        res,value, pred = fungsi.predict_glcm(img)
        ori = ImageTk.PhotoImage(Image.open(str(res['original'])).resize((100,100)))
        panel_ori.configure(image=ori)
        panel_ori.image = ori
        gray = ImageTk.PhotoImage(Image.open(str(res['gray'])).resize((100,100)))
        panel_gray.configure(image=gray)
        panel_gray.image = gray
        rsz = ImageTk.PhotoImage(Image.open(str(res['resize'])).resize((100,100)))
        panel_rsz.configure(image=rsz)
        panel_rsz.image = rsz
        hist = ImageTk.PhotoImage(Image.open(str(res['histogram'])).resize((100,100)))
        panel_hist.configure(image=hist)
        panel_hist.image = hist
        for val in value:
            # print(val)
            tree.insert('', tk.END, values=val)
        prediction['text'] = pred
    elif img=='':
        messagebox.showerror("Error","File must fill")
        trigger_entry.delete(0, 'end')
    else:
        messagebox.showerror("Error","File must be image")
        trigger_entry.delete(0, 'end')

def reset():
    prediction['text'] = "HASIL"
    ori = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
    panel_ori.configure(image=ori)
    panel_ori.image = ori
    gray = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
    panel_gray.configure(image=gray)
    panel_gray.image = gray
    rsz = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
    panel_rsz.configure(image=rsz)
    panel_rsz.image = rsz
    hist = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
    panel_hist.configure(image=hist)
    panel_hist.image = hist
    for item in tree.get_children():
        tree.delete(item)
    trigger_entry.delete(0, 'end')
    

# trigger
lbl_trigger = Label(frame_fields,text='Select Image',font=('bold','12'))
lbl_trigger.grid(row=0,column=0,sticky=N)
trigger = StringVar()
trigger_entry = Entry(frame_fields,textvariable=trigger,width=40)
trigger_entry.grid(row=0,column=1,sticky=N)

trigger_path_button = Button(frame_fields, text='Select', width=12, command=trigger_file)
trigger_path_button.grid(row=0,column=2,sticky='ns',padx=5)

submit_button = Button(frame_fields, text='Submit', width=12, command=callback)
submit_button.grid(row=1,column=1, sticky=E)
submit_button = Button(frame_fields, text='Reset', width=12, command=reset)
submit_button.grid(row=1,column=2,pady=15)


frame_img = LabelFrame(frame_div,text="Image Pre-Processing")
frame_img.grid(row=1,column=0,sticky=N,pady=(60,5))

image1 = Image.open("tmp/no.jpg")
image2 = image1.resize((100,100))
test = ImageTk.PhotoImage(image2)

# canvas ori
no_ori = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
panel_ori = tk.Label(frame_img, image=no_ori, width = 100, height = 100)
panel_ori.grid(row=0,column=0)
lbl_ori = Label(frame_img,text='Image Original',font=('bold','12'))
lbl_ori.grid(row=1,column=0,sticky=N,padx=5)

# canvas gray
no_gray = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
panel_gray = tk.Label(frame_img, image=no_gray, width = 100, height = 100)
panel_gray.grid(row=0,column=1)
lbl_gray = Label(frame_img,text='Image Grayscale',font=('bold','12'))
lbl_gray.grid(row=1,column=1,sticky=N,padx=5)

# canvas resize
no_rsz = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
panel_rsz = tk.Label(frame_img, image=no_rsz, width = 100, height = 100)
panel_rsz.grid(row=2,column=0)
lbl_rsz = Label(frame_img,text='Image Resize',font=('bold','12'))
lbl_rsz.grid(row=3,column=0,sticky=N,padx=5)


# canvas histogram eq
no_hist = ImageTk.PhotoImage(Image.open("tmp/no.jpg").resize((100,100)))
panel_hist = tk.Label(frame_img, image=no_hist, width = 100, height = 100)
panel_hist.grid(row=2,column=1,sticky=N,padx=5)
lbl_hist = Label(frame_img,text='Image Histogram',font=('bold','12'))
lbl_hist.grid(row=3,column=1,sticky=N,padx=5)

frame_div1 = Frame(frame_body)
frame_div1.grid(row=0,column=1,sticky=tk.NW,padx=20)
frame_button = Frame(frame_div1)
frame_button.grid(row=0,column=0,sticky=N)

# define columns
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

prediction = Button(frame_button,text='HASIL', width=10,font=('bold','20'), state='disable')
prediction.grid(row=1,column=0,sticky='e',pady=10)

root.mainloop()

