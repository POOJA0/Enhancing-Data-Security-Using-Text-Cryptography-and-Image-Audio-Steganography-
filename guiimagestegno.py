import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import numpy as np
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from LSBSteg import LSBSteg
import cv2
from wavsteg import hide_data
from wavsteg import recover_data
import os
from tkinter import messagebox
from math import log10, sqrt
import matplotlib.pyplot as plt
import matplotlib.image as img


def browseTextFile():
    global filenametohide
    global statuslabel
    filenametohide = fd.askopenfilename(filetypes = (('text files','*.txt'),))
    statuslabel.config(text="text selected")
    

def browseCoverImage():
    global coverfile
    global statuslabel
    coverfile = fd.askopenfilename(filetypes = (('image files','*.png'),))
    statuslabel.config(text="cover selected")

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
                  # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def MSE(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    return mse
    
def doEncryptAndEmbed():
    global filenametohide
    global coverfile
    global e1,e2

    keys=e1.get()
    key=bytes(keys, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC)

    ks=len(key)
    if ks!=16:
        messagebox.showerror("Error", "key should be 16 characters")
        return
        
    text_file = open(filenametohide, "r")
    data = text_file.read()
    text_file.close()

    bdata=bytes(data,'utf-8')
    ciphered_data = cipher.encrypt(pad(bdata, AES.block_size))

    
    file_out = open('tempb', "wb") 
    file_out.write(cipher.iv) 
    file_out.write(ciphered_data) 
    file_out.close()

    output_file = e2.get()
    steg = LSBSteg(cv2.imread(coverfile))
    data = open("tempb", "rb").read()
    new_img = steg.encode_binary(data)
    cv2.imwrite(output_file, new_img)

    original = cv2.imread(coverfile)
    compressed = cv2.imread(output_file)
    
    msev=MSE(original,compressed)
    psnrv=PSNR(original,compressed)

    mselabel.config(text="MSE:"+str(msev))
    psnrlabel.config(text="PSNR:" + str(psnrv))

    fig = plt.figure()
    ax1 = fig.add_subplot(1,2,1)
    ax1.imshow(img.imread(coverfile))
    ax2 = fig.add_subplot(1,2,2)
    ax2.imshow(img.imread(output_file))

    plt.show()
    
    
def browseSecretImage():
    global secretfile
    secretfile = fd.askopenfilename(filetypes = (('image files','*.png'),))
    statuslabel.config(text="secret image selected")
    
def dodecrypt():
    global secretfile
    
    keys=e1.get()
    key=bytes(keys, 'utf-8')
    ks=len(key)
    if ks!=16:
        messagebox.showerror("Error", "key should be 16 characters")
        return
    
    steg = LSBSteg(cv2.imread(secretfile))
    binary = steg.decode_binary()
    file_out = open("recovered.bin", "wb")
    file_out.write(binary);
    file_out.close()


    file_in = open("recovered.bin", 'rb') # Open the file to read bytes
    iv = file_in.read(16) # Read the iv out - this is 16 bytes long
    ciphered_data = file_in.read() # Read the rest of the data
    file_in.close()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
    original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result

    txtdata=original_data.decode('utf-8')

    #open text file
    text_file = open("decryptedfile.txt", "w")
 
    #write string to file
    text_file.write(txtdata)
 
    #close file
    text_file.close()
        
    messagebox.showinfo("showinfo", "decoded content written to decryptedfile.txt ")

    
    
    
if __name__ == "__main__":
    global parent
    global label
    global e1,e2,e3,e4,variable
    global mselabel
    global psnrlabel
    global filenametohide
    global coverfile
    global secretfile
    global statuslabel

    parent = tk.Tk()
    parent.geometry("600x600")
    parent.configure(bg='black')
    parent.title("Image steganography")

    frame = tk.Frame(parent)
    frame.pack()

    w = tk.Label(frame, text="Image steganography",
                     fg = "red",
                     font = ("Times New Roman", 18))
    w.pack()

    w=tk.Label(frame, 
             text="Secrety key (of length 16 characters")
    w.pack()
    e1 = tk.Entry(frame)
    e1.pack()

    w=tk.Label(frame, 
             text="")
    w.pack() 

    # Separator object
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x')

    
    
    

    w=tk.Label(frame, 
             text="EMBEDDING")
    w.pack()


    w=tk.Label(frame, 
             text="")
    w.pack()



    text_disp= tk.Button(frame, 
                       text="BROWSE TEXT FILE TO HIDE", 
                       command=browseTextFile
                       )
    text_disp.pack()


    w=tk.Label(frame, 
             text="")
    w.pack()
    
    text_disp= tk.Button(frame, 
                       text="BROWSE COVER IMAGE", 
                       command=browseCoverImage
                       )
    text_disp.pack()

    w=tk.Label(frame, 
             text="")
    w.pack()
      
    w=tk.Label(frame, 
             text="File name to save secret image(.png)")
    w.pack()
    e2 = tk.Entry(frame)
    e2.pack()

    statuslabel=tk.Label(frame, 
             text="",fg="blue")
    statuslabel.pack()

    
     
    text_disp= tk.Button(frame, 
                       text="ENCRYPT AND EMBEED", 
                       command=doEncryptAndEmbed
                       )
    text_disp.pack()
      
    w=tk.Label(frame, 
             text="")
    w.pack()


    w=tk.Label(frame, 
             text="")
    w.pack()


    mselabel = tk.Label(frame, fg="red")
    mselabel.pack()

    psnrlabel = tk.Label(frame, fg="red")
    psnrlabel.pack()
    

    # Separator object
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x')

    w=tk.Label(frame, 
             text="DE-EMBEDDING")
    w.pack()

    w=tk.Label(frame, 
             text="")
    w.pack()

    text_disp= tk.Button(frame, 
                       text="BROWSE SECRET IMAGE", 
                       command=browseSecretImage
                       )
    text_disp.pack()
    
    w=tk.Label(frame, 
             text="")
    w.pack()
     
    text_disp= tk.Button(frame, 
                       text="DEEMBED AND DECRYPT", 
                       command=dodecrypt
                       )
    text_disp.pack()
    
    
    parent.mainloop()

    
    

