# Importing necessary packages
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

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
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

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