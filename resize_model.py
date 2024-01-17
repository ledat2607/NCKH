import os
import cv2

input_folder = 'Resources/Modes'
output_folder = 'Resources/Models'
target_width = 414
target_height = 633

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is an image (you might want to improve this check based on your file types)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Read the image
        img = cv2.imread(input_path)

        # Resize the image
        resized_img = cv2.resize(img, (target_width, target_height))

        # Save the resized image
        cv2.imwrite(output_path, resized_img)

print("Resizing complete.")
