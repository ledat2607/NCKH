import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(3, 480)
#format size
target_size = (240, 240)
while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture frame")
        break
    #resize image before recog by farme
    img_resized = cv2.resize(img, target_size)
    cv2.imshow("Face Attendance", img_resized)
    key = cv2.waitKey(1)
    if key == 27:  # 27 is the ASCII code for 'Esc'
        break
cap.release()
cv2.destroyAllWindows()
