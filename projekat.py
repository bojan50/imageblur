import cv2
import easygui
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import *

ekran=tk.Tk()
ekran.geometry('400x400')
ekran.title('Ćipović Bojan RIN 11/20')
bg = PhotoImage(file = "pozadina.png")
label1=Label(ekran, image=bg)
label1.place(x = -5, y = -2)

def upload():
    ImagePath=easygui.fileopenbox()
    crtaj(ImagePath)

def crtaj(ImagePath):

    image1 = cv2.imread(ImagePath)
    grayImage = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    grayImage = cv2.GaussianBlur(grayImage, (3, 3), 0)
    edgeImage = cv2.Laplacian(grayImage, -1, ksize=5)
    edgeImage = 255 - edgeImage
    edgePreservingImage = cv2.edgePreservingFilter(image1, flags= 2, sigma_s=50, sigma_r=0.4)
    output = np.zeros(grayImage.shape)
    output = cv2.bitwise_and(edgePreservingImage, edgePreservingImage, mask=edgeImage)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
    image2 = cv2.resize(edges, (960, 540))
    color = cv2.bilateralFilter(image1, 12, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cartoon_image = cv2.stylization(image1, sigma_s=150, sigma_r=0.25)
    image3 = cv2.resize(cartoon_image, (960, 540))
    blurred = cv2.bilateralFilter(image1, d=7, sigmaColor=200, sigmaSpace=200)
    cartoon_image = cv2.bitwise_and(blurred, blurred, mask=edges)
    cartoon_image1, cartoon_image2 = cv2.pencilSketch(image1, sigma_s=60, sigma_r=0.4, shade_factor=0.01)
    image4 = cv2.resize(cartoon_image2, (960, 540))
    cv2.imshow('pencil', cartoon_image)
    images=[image1, image2, image3, image4]

    fig, axes = plt.subplots(2, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    btn2 = Button(ekran, text = 'Sacuvaj sliku!', command = lambda: save(image3, ImagePath), padx=30 , pady=5 )
    btn2.configure(background='#364156', foreground='white', font=('calibri',12,'bold'))
    btn2.pack(side=TOP,pady=50)
    plt.show()

#cuva sliku u direktorijumu odakle je izabrana prvobitna slika pod nazivom 'gotova slika'
def save(image3, ImagePath):
    newName = 'Gotova slika'
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(image3, cv2.COLOR_BGR2BGRA))
    I = "Slika sacuvana" + newName + "u " + path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(ekran,text="Izaberi sliku",command=upload,padx=15,pady=15)
upload.configure(background='red', foreground='white',font=('calibri',12,'bold'))
upload.pack(side=TOP,pady=50)

ekran.mainloop()