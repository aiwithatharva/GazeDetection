import os
from PIL import Image
from tqdm import tqdm  # Import tqdm

# Paths to your dataset directories
train_txt_file = 'path/to/your/train_annotations.txt'
test_txt_file = 'path/to/your/test_annotations.txt'
images_dir = 'path/to/your/images'
train_labels_dir = 'path/to/your/train_labels'
test_labels_dir = 'path/to/your/test_labels'

# Create label directories if they don't exist
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(test_labels_dir, exist_ok=True)

def convert_to_yolo_format(xmin, ymin, width, height, img_width, img_height):
    # Convert pixel coordinates to normalized coordinates
    x_center = (xmin + width / 2) / img_width
    y_center = (ymin + height / 2) / img_height
    norm_width = width / img_width
    norm_height = height / img_height

    return x_center, y_center, norm_width, norm_height

def save_annotation(image_name, coords, labels_dir):
    # Save to YOLO format .txt file
    label_file = os.path.join(labels_dir, os.path.splitext(image_name)[0] + '.txt')
    with open(label_file, 'w') as f:
        # Assuming class_id is 0 for a single class
        f.write(f"0 {coords[0]} {coords[1]} {coords[2]} {coords[3]}\n")

def process_txt(txt_file, labels_dir):
    with open(txt_file, 'r') as file:
        lines = file.readlines()
    
    for line in tqdm(lines, desc=f'Processing {os.path.basename(txt_file)}'):
        # Split line by comma
        parts = line.strip().split(',')
        image_path = parts[0]
        xmin = float(parts[1])
        ymin = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        # Load image to get dimensions
        image_file = os.path.join(images_dir, image_path)
        img = Image.open(image_file)
        img_width, img_height = img.size

        # Convert and save annotations
        x_center, y_center, norm_width, norm_height = convert_to_yolo_format(xmin, ymin, width, height, img_width, img_height)
        save_annotation(os.path.basename(image_path), (x_center, y_center, norm_width, norm_height), labels_dir)

# Process training and test datasets
process_txt(train_txt_file, train_labels_dir)
process_txt(test_txt_file, test_labels_dir)

print("Conversion completed.")
