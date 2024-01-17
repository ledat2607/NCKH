import os
import pickle
import numpy as np
import cv2
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials, db, storage
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")
display_date = datetime.strptime(current_date, "%Y-%m-%d").strftime("%d-%m")
# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://facerego-27f4b-default-rtdb.firebaseio.com/','storageBucket':"facerego-27f4b.appspot.com"})
bucket = storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')
font_path_vietnamese = "UVNBaiSau_R.TTF"
font_size = 32
font_color = (0, 0, 0)

# Load a Vietnamese font
font = ImageFont.truetype(font_path_vietnamese, font_size)
# Load images from resources
folderModePath = 'Resources/Models'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Import encode file
print("Loading Encoding file....")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Load Complete...")


# Get the current date and time
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")

modeType = 0
counter = 0
id = -1
imgStudent = []
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)
            #Đánh dấu vị trí gương mặt
            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        #Lấy thông tin
    if counter != 0:
        if counter == 1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
            #Lấy hình ảnh theo ID
            blob = bucket.get_blob(f'faceStudent/{id}.png')
            array = np.frombuffer(blob.download_as_string(),np.uint8)
            imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
            #Thêm mới dữ liệu nếu chưa có dữ liệu
            current_date_exists = any(info['current_date'] == current_date for info in studentInfo.get('attendance', []))
            if not current_date_exists:
                # If not, create a new entry for the current date
                new_attendance_entry = {
                    'current_date': current_date,
                    'total_attendance': 1,  # Set initial total attendance to 0
                    'check_in_time': current_time,  # You may set this to an appropriate default value
                    'check_in':True,
                    'last_attendance':current_time,
                    # Add other fields as needed
                }
                studentInfo['attendance'].append(new_attendance_entry)
            else:
                for attendance_info in studentInfo['attendance']:
                    if attendance_info['current_date'] == current_date:
                        attendance_info['total_attendance'] += 1

            db.reference(f'Students/{id}').set(studentInfo)  # Update the database
            # Refresh studentInfo after updating the database
            studentInfo = db.reference(f'Students/{id}').get()

        if 10 < counter < 15:
            modeType = 2
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        if counter < 5:
            for attendance_info in studentInfo['attendance']:
                date = attendance_info['current_date']
                total_attendance = attendance_info['total_attendance']

                # Hiển thị chỉ khi ngày trùng khớp với ngày hiện tại
                if date == current_date:
                    attendance_info['last_attendance'] = current_time # Set the last attendance time
                    db.reference(f'Students/{id}/attendance').set(studentInfo['attendance'])  # Update the database
                    text_to_display = f"{total_attendance}"
                    cv2.putText(imgBackground, text_to_display, (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, f"Check out:{attendance_info['last_attendance']}", (921, 655), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (0, 0, 0), 1)
                    cv2.putText(imgBackground, f"{attendance_info['check_in_time']}", (905, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgBackground, f"{attendance_info['current_date']}", (1110, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

                    cv2.putText(imgBackground, f"{studentInfo['mssv']}", (906, 498),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)
                    cv2.putText(imgBackground, f"{studentInfo['major']}", (976, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(imgBackground, f"{studentInfo['starting_year']}", (1010, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    (w, h), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414-w)//2
                    image_pil = Image.fromarray(imgBackground)
                    draw = ImageDraw.Draw(image_pil)
                    draw.text((848 + offset, 405), studentInfo['name'], font=font, fill=(0, 0, 0))

                    imgBackground = np.array(image_pil)
                    attendance_updated_for_loop = True
            imgBackground[175:175+216,909:909+216] = imgStudent
        counter += 1
        if counter >= 16:
            counter = 0
            modeType = 0
            studentInfo = []
            imgStudent = []
    cv2.imshow("Face Attendance", imgBackground)
    key = cv2.waitKey(1)

    if key == 27 or key == ord('q'):  # 27 is the ASCII code for esc
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
