import tkinter as tk
import cv2
from fpdf import FPDF
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import sys
import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig


from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

import keras
import os

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename


def pdfgenerator(image,data, predval):
    image = Image.open(image)
    new_image = image.resize((400, 400))
    new_image.save('image2.jpg')     
        
    if (predval > 0.5):
        classifier = 'Normal ' + str(predval)
    else:
        classifier = 'Abnormal ' + str(predval)

    
    patient_name = data[0]
    gender = data[1]
    DOB = data[2]
    address = data[3]
    physician_name = data[4]
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(5)
    #pdf.image('/Users/udaytripathi/Desktop/otoAI_logo.png', x = None, y = None, w = 20, h = 0, type = '', link = '')
    
    pdf.cell(60)
    pdf.cell(90, 10, "OtoAI Ear Exam Results and Preliminary Diagnosis", 0, 2, 'C')
    pdf.cell(90, 2, " ", 0, 2, 'C')
    pdf.cell(-40)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(160, 10, 'Patient Name:' + " " + patient_name, 1, 2, 'L')
    pdf.cell(160, 10, 'Gender:' + " " + gender, 1, 2, 'L')
    pdf.cell(160, 10, 'Date of Birth (MM/DD/YYYY):' + " " + DOB, 1, 2, 'L')
    pdf.cell(160, 10, 'Address:' + " " + address, 1, 2, 'L')
    pdf.cell(160, 10, 'Physician Name:' + " " + physician_name, 1, 2, 'L')
    pdf.cell(-120)
    pdf.set_font('helvetica', '', 12)

    pdf.cell(-70)
    pdf.cell(90, 5, " ", 0, 2, 'C')
    pdf.cell(200)
    pdf.image('image2.jpg', x = None, y = None, w = 0, h = 0, type = '', link = '')
    
    pdf.cell(90, 2, " ", 0, 2, 'C')
    pdf.cell(140, 10, 'Classification: '+ '%s' % classifier, 1, 2, 'C')
    pdf.cell(140, 10, 'Percent Confidence: '  '%s' % '90%', 1, 2, 'C')
    
    pdf.cell(90,5, " ", 0, 2, 'C')
    pdf.cell(-20)
    pdf.set_font('helvetica', '', 8)
    pdf.cell(40)
    pdf.cell(90,10,"While the OtoAI algorithm is robust in nature, patients should refer to their primary care physicians for next steps",0,2,'C')
    pdf.output('output.pdf', 'F')

def image_capture():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

#histogram equalization to improve contrast
def improve_contrast_image_using_clahe(bgr_image):
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    hsv_planes = cv2.split(hsv)
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(7, 7))
    hsv_planes[2] = clahe.apply(hsv_planes[2])
    hsv = cv2.merge(hsv_planes)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def image_enhancement(image):
    ####CROP, CONTRAST, and ENHANCE
    images = [image] #input appropriate image name(s)
    for name in images:

        img = cv2.imread(name)

        ###CONTRAST
        improved = img
        #improved = improve_contrast_image_using_clahe(img)

        ###CROP
        gray = cv2.cvtColor(improved, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
        # Find contour and sort by contour area
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # Find bounding box and extract ROI
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            ROI = improved[y:y+h, x:x+w]
            break

        final = cv2.resize(ROI,(150, 150))
        final = final.astype("float") #/ 255.0

        cv2.imwrite('image_enhanced2.jpg',final)

def proceed_image():
    patient_name = patient_name_1.get()
    gender = gender_1.get()
    dob = dob_1.get()
    address = address_1.get()
    physician_name = physician_name_1.get()
    
    global data
    data = [patient_name, gender, dob, address, physician_name]
    
    master.destroy()    
             
    # input_image = filename
    # image_enhancement(input_image)
    
    # enhanced = cv2.imread('image_enhanced2.jpg')
    # enhanced = enhanced.astype("float") / 255.0
    
    # image = keras.preprocessing.image.img_to_array(enhanced)
    # image = np.expand_dims(image, axis=0)
    # model = keras.models.load_model('C:\\Users\\nmahe\\Documents\\SeniorDesignOtoscope\\saved-model-88-0.90.hdf5')
    
    # #make prediction
    # pred = model.predict(image)
    # print(pred)        
    
    
    # pdfgenerator('image_enhanced2.jpg',data, pred)
    
    # sys.exit()
    
# Defining CreateWidgets() function to create necessary tkinter widgets
def CreateWidgets():

    root.feedlabel = Label(root, bg="steelblue", fg="white",
                           text='''1: Browse To Select Save Directory
    2: Press any Key to Capture Image''', font=('Times',20))
    root.feedlabel.grid(row=4, column=4, padx=10, pady=10, columnspan=2)

    root.feedlabel = Label(root, bg="steelblue", fg="white", text="Otoscope Camera Feed", font=('Times',20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.saveLocationEntry = Entry(root, width=55, textvariable=destPath)
    root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)

    root.browseButton = Button(root, width=10, text="BROWSE", command=destBrowse)
    root.browseButton.grid(row=3, column=2, padx=10, pady=10)

    root.captureBTN = Button(root, text="CAPTURE", command=Capture, bg="LIGHTBLUE", font=('Times',15), width=20)
    root.captureBTN.grid(row=4, column=1, padx=10, pady=10)

    root.RPTBTN = Button(root, text="Generate Report", command=Generate_Report, bg="LIGHTBLUE", font=('Times',15), width=13)
    root.RPTBTN.grid(row=4, column=2)

    root.previewlabel = Label(root, bg="steelblue", fg="white", text="Image Preview", font=('Times',20))
    root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

    root.imageLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

    root.openImageEntry = Entry(root, width=55, textvariable=imagePath)
    root.openImageEntry.grid(row=3, column=4, padx=10, pady=10)

    root.openImageButton = Button(root, width=10, text="BROWSE", command=imageBrowse)
    root.openImageButton.grid(row=3, column=5, padx=10, pady=10)

    try:
        logo = PhotoImage(file='OtoAI_Logo.png')
        root.imageLabel.config(image=logo)
    except:
        print("Please Add OtoAI image to Path")
        
    ShowFeed()

# Defining ShowFeed() function to display webcam feed in the cameraLabel;
def ShowFeed():
    # Capturing frame by frame
    ret, frame = root.cap.read()

    if ret:
        # Flipping the frame vertically
        frame = cv2.flip(frame, 1)

        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

        # Changing the frame color from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Creating an image memory from the above frame exporting array interface
        videoImg = Image.fromarray(cv2image)

        # Creating object of PhotoImage() class to display the frame
        imgtk = ImageTk.PhotoImage(image = videoImg)

        # Configuring the label to display the frame
        root.cameraLabel.configure(image=imgtk)

        # Keeping a reference
        root.cameraLabel.imgtk = imgtk

        # Calling the function after 10 milliseconds
        root.cameraLabel.after(10, ShowFeed)
    else:
        # Configuring the label to display the frame
        root.cameraLabel.configure(image='')

def destBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")

    # Displaying the directory in the directory textbox
    destPath.set(destDirectory)
    root.focus_force()

def imageBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    openDirectory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")

    # Displaying the directory in the directory textbox
    imagePath.set(openDirectory)

    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    imageView = Image.open(openDirectory)

    # Resizing the image using Image.resize()
    imageResize = imageView.resize((640, 480), Image.ANTIALIAS)

    # Creating object of PhotoImage() class to display the frame
    imageDisplay = ImageTk.PhotoImage(imageResize)

    # Configuring the label to display the frame
    root.imageLabel.config(image=imageDisplay)

    # Keeping a reference
    root.imageLabel.photo = imageDisplay
    root.focus_force()

def Show_im(imgName):
    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    saved_image = Image.open(imgName)
    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image)
    # Configuring the label to display the frame
    root.imageLabel.config(image=saved_image)
    # Keeping a reference
    root.imageLabel.photo = saved_image

# Defining Capture() to capture and save the image and display the image in the imageLabel
def Capture(event=None):
    # Storing the date in the mentioned format in the image_name variable
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

    image_path = destPath.get()

    # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
    imgName = image_path + '/' + image_name + ".jpg"

    # Capturing the frame
    ret, frame = root.cap.read()

    # Displaying date and time on the frame
    #cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

    # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
    success = cv2.imwrite(imgName, frame)

    if success:
        Show_im(imgName)
    else:
        messagebox.showinfo("Failure", "Image NOT Captured")


# Defining StopCAM() to stop WEBCAM Preview
def Generate_Report():
    if imagePath.get() != '':
        print("Path To Classifier: " + imagePath.get())
        input_image = imagePath.get()
        image_enhancement(input_image)
        
        enhanced = cv2.imread('image_enhanced2.jpg')
        enhanced = enhanced.astype("float") / 255.0
        
        image = keras.preprocessing.image.img_to_array(enhanced)
        image = np.expand_dims(image, axis=0)
        model = keras.models.load_model('C:\\Users\\nmahe\\Documents\\SeniorDesignOtoscope\\saved-model-88-0.90.hdf5')
        
        #make prediction
        pred = model.predict(image)
        print(pred)        
        
        
        pdfgenerator('image_enhanced2.jpg',data, pred)
        
    else:
        messagebox.showinfo("ERROR", "Browse for Image to Classify")

def StartCAM():
    # Creating object of class VideoCapture with webcam index
    root.cap = cv2.VideoCapture(0)

    # Setting width and height
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)

    # Removing text message from the camera label
    root.cameraLabel.config(text="")

    # Calling the ShowFeed() Function
    ShowFeed()
    
master = tk.Tk()
tk.Label(master, text="Patient Name:").grid(row=0)
tk.Label(master, text="Gender:").grid(row=1)
tk.Label(master, text="DOB (MM/DD/YYYY):").grid(row=2)
tk.Label(master, text="Address:").grid(row=3)
tk.Label(master, text="Physician's Name:").grid(row=4)

patient_name_1 = tk.Entry(master)
gender_1 = tk.Entry(master)
dob_1 = tk.Entry(master)
address_1 = tk.Entry(master)
physician_name_1 = tk.Entry(master)

patient_name_1.grid(row=0, column=1)
gender_1.grid(row=1, column=1)
dob_1.grid(row=2, column=1)
address_1.grid(row=3, column=1)
physician_name_1.grid(row=4, column=1)

tk.Button(master, 
          text='Proceed', command=proceed_image).grid(row=5, 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)
master.mainloop()

# Creating object of tk class
root = tk.Tk()

# Creating object of class VideoCapture with webcam index
root.cap = cv2.VideoCapture(0)

# Setting width and height
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Setting the title, window size, background color and disabling the resizing property
root.geometry("1340x670")
root.resizable(True, True)
root.title("OtoAI Image Capture and Classification")
root.configure(background = "steelblue")

# Creating tkinter variables
destPath = StringVar()
imagePath = StringVar()

# Calling the CreateWidgets() function
CreateWidgets()
destBrowse()
# Defining infinite loop to run application
root.bind('<Key>', Capture)
root.mainloop()

os.startfile('output.pdf')


