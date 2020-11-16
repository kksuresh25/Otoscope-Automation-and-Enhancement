import cv2
from fpdf import FPDF
from PIL import Image
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def pdfgenerator(image,data):
    image = Image.open(image)
    new_image = image.resize((400, 400))
    new_image.save('image2.jpg')

    if (data == 1):
        classifier = 'Normal'
        action = 'Stay at home'
    else:
        classifier = 'Abnormal'
        action = 'Please see your PCP'


    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    pdf.cell(60)
    pdf.cell(100, 10, "OtoAI Ear Exam Results and Preliminary Diagnoses", 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-40)
    pdf.cell(60, 10, 'Preliminary Diagnosis', 1, 0, 'C')
    pdf.cell(60, 10, 'Percent Confidence', 1, 0, 'C')
    pdf.cell(60, 10, 'Special Instructions', 1, 2, 'C')
    pdf.cell(-120)
    pdf.set_font('arial', '', 12)
    pdf.cell(60, 10, '%s' % classifier, 1, 0, 'C')
    pdf.cell(60, 10, '%s' % '85%', 1, 0, 'C')
    pdf.cell(60, 10, '%s' % action, 1, 2, 'C')
    pdf.cell(-70)
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-30)
    pdf.image('image2.jpg', x = None, y = None, w = 0, h = 0, type = '', link = '')
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
        improved = improve_contrast_image_using_clahe(img)

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
        cv2.imwrite('image_enhanced.jpg',ROI)


####MAIN####
image_capture()
image_enhancement('opencv_frame_0.png')
pdfgenerator('image_enhanced.jpg',1)
