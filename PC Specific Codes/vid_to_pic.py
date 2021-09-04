import cv2

cap = cv2.VideoCapture(r'C:\Users\NCETIS\Documents\MATLAB\Media3_cropped2.avi')
i=0
while(i<500):
    _,im = cap.read()
    i+=1
    #r = cv2.selectROI(im)
    #imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    cv2.imwrite(str(i)+'.jpg',im,None)


cap.release()