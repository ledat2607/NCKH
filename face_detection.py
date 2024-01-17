import os
import cv2
import dlib

# Hàm cắt gương mặt từ ảnh dùng thư viện dlib
def crop_face_dlib(image_path, output_folder, target_size=(216, 216)):
    # Đọc ảnh từ đường dẫn
    image = cv2.imread(image_path)
    # Tạo bộ phát hiện khuôn mặt từ dlib
    detector = dlib.get_frontal_face_detector()
    # Chuyển đổi ảnh sang ảnh đen trắng để tăng hiệu suất
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Phát hiện khuôn mặt trong ảnh
    faces = detector(gray_image)
    # Lặp qua các khuôn mặt và cắt từng khuôn mặt
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        face_roi = image[y:y + h, x:x + w]

        # Resize khuôn mặt về kích thước mong muốn
        face_resized = cv2.resize(face_roi, target_size)

        # Lưu khuôn mặt cắt ra thành một file mới trong thư mục đầu ra
        output_path = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(image_path))[0]}.png')
        cv2.imwrite(output_path, face_resized)

# Thư mục chứa hình ảnh ban đầu
input_folder = 'images/'

# Thư mục để lưu hình ảnh đã cắt
output_folder = 'faceStudent/'

# Tạo thư mục đầu ra nếu nó chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lặp qua tất cả các tệp hình ảnh trong thư mục đầu vào
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        # Tạo đường dẫn đầy đủ đến ảnh
        image_path = os.path.join(input_folder, filename)

        # Gọi hàm cắt gương mặt cho mỗi ảnh trong thư mục
        crop_face_dlib(image_path, output_folder)

# Hiển thị xong tất cả ảnh
print("Đã cắt gương mặt từ tất cả các ảnh trong thư mục.")
