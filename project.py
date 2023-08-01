import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

# New window
root = tk.Tk()
root.title("Wheatstone Bridge")

# Window size
root.geometry('800x600')

# open image
image = Image.open('wheatstone.png')

# PhotoImage object 
photo = ImageTk.PhotoImage(image)

# Canvas widget
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack()

# Add pic to canvas
canvas.create_image(0, 0, image=photo, anchor=tk.NW)

# Info window (I didnt change it to english, not very useful for u Xd)
def show_info():
    messagebox.showinfo("O programu", "Ovo je Wheatstoneov most za mjerenje otpora. Sastoji se od dobro poznatog strujnog kruga koji sadrži bateriju, četiri otpornika i jednog galvanometra. Tri otpornika su poznatih otpora, a četvrti ima nepoznati otpor. Galvanometar služi mjerenju razlike potencijala između dvaju grana strujnog kruga pa se često naziva i mostom (Wheatstoneov most). Upišite željene vrijednosti otpornika R1 i R2, željeni napon izvora i pomičite kliznik sve dok ne dobijete približnu razliku potencijala od 0V. Očitajte nepoznati otpor Rx!")

info_button = tk.Button(root, text="Info", command=show_info)
info_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Input box for Vs(voltage source), R1(Resistor 1), R2(Resistor 2)
vs_label = tk.Label(root, text="Vs=")
vs_label.place(x=500, y=350)
vs = tk.Entry(root)
vs.insert(0, "5.0")  # default value on beggining
vs.place(x=530, y=350)

def update_vs():
    global Vs
    try:
        Vs = float(vs.get())
    except ValueError:
        pass
    
r1_label = tk.Label(root, text="R1=")
r1_label.place(x=500, y=450)
r1 = tk.Entry(root)
r1.insert(0, "100.0")  # Default value
r1.place(x=530, y=450)

def update_r1():
    try:
        r1_val = float(r1.get())
        update_rx(r3_slider.get())  # Update Rx when R1 is changed
    except ValueError:
        pass

r2_label = tk.Label(root, text="R2=")
r2_label.place(x=500, y=500)
r2 = tk.Entry(root)
r2.insert(0, "1000.0")  # Default value
r2.place(x=530, y=500)

def update_r2():
    try:
        r2_val = float(r2.get())
        update_rx(r3_slider.get())  # Update Rx when R2 is changed
    except ValueError:
        pass
    
# Slider R3
r3_label = tk.Label(root, text="R3:")
r3_label.place(x=20, y=460)
r3_slider = tk.Scale(root, from_=1, to=1000, resolution=1, orient=tk.HORIZONTAL, length=200)
r3_slider.place(x=50, y=450)

def update_r3(event):
    try:
        r3_val = float(r3_slider.get())
        vs_val = float(vs.get())
        r1_val = float(r1.get())
        r2_val = float(r2.get())
        print(f"r3_val: {r3_val}, vs_val: {vs_val}, r1_val: {r1_val}, r2_val: {r2_val}")
        rx_val = (r3_val * r2_val) / r1_val
        vd_val = (vs_val * r2_val) / (r1_val + r2_val) - (vs_val * rx_val) / (r3_val + rx_val)
        vd_label.config(text="Vd = {:.2f}".format(vd_val))
        update_rx(r3_val)
    except ValueError:
        pass

r3_slider.bind("<ButtonRelease-1>", update_r3)
    
    
# Label for showing Rx values
rx_label = tk.Label(root, text="Rx = ")
rx_label.place(x=500, y=560)

# Potential difference
vd_label = tk.Label(root, text="Vd = ")
vd_label.place(x=500, y=400)

# Calculating Rx and update
def update_rx(r3_val):
    try:
        vs_val = float(vs.get())
        r1_val = float(r1.get())
        r2_val = float(r2.get())
        rx_val = (float(r3_val) * r2_val) / r1_val
        rx_label.config(text="Rx = {:.2f}".format(rx_val))
    except ZeroDivisionError:
        pass

def calculate_vd(vs_val, r1_val, r2_val, r3_val, rx_val):
    if r3_val == 0:
        vd = 0
    else:
        vd = vs_val * (((r2_val)/(r1_val+r2_val))-((rx_val)/(r3_val+rx_val)))
    return vd


# Buttons for update
vs_button = tk.Button(root, text="Update Vs", command=update_vs)
vs_button.place(x=650, y=350)

r1_button = tk.Button(root, text="Update R1", command=update_r1)
r1_button.place(x=650, y=450)

r2_button = tk.Button(root, text="Update R2", command=update_r2)
r2_button.place(x=650, y=500)

vs.bind("<Return>", update_vs)
# Connection between update_rx and slider
r3_slider.config(command=update_rx)
update_rx(r3_slider.get())
# Start loop
root.mainloop()
