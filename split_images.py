import csv
from PIL import Image
import os

def get_chunk_coordinates(x, y, x_step, y_step, ul_lon, ul_lat, lr_lon, lr_lat):
    """Calculate coordinates for each chunk."""
    x_ratio = x / x_step
    y_ratio = y / y_step

    chunk_ul_lon = ul_lon + x_ratio * (lr_lon - ul_lon)
    chunk_ul_lat = ul_lat + y_ratio * (ul_lat - lr_lat)
    chunk_lr_lon = chunk_ul_lon + (lr_lon - ul_lon) / x_step
    chunk_lr_lat = chunk_ul_lat + (lr_lat - ul_lat) / y_step

    return chunk_ul_lon, chunk_ul_lat, chunk_lr_lon, chunk_lr_lat

input_csv = "original_geojpg.csv"
output_csv = "final_geojpg.csv"
input_folder = "ee_original_images"
rotated_folder = "rotated_images"
split_folder = "split_images"

# Ensure the folders exist
if not os.path.exists(rotated_folder):
    os.makedirs(rotated_folder)
if not os.path.exists(split_folder):
    os.makedirs(split_folder)

with open(input_csv, "r") as f_in, open(output_csv, "w", newline='') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    writer.writerow(["filename", "ul_lat", "ul_lon", "ur_lat", "ur_lon", "ll_lat", "ll_lon", "lr_lat", "lr_lon"])
    
    next(reader)  # skip header
    for row in reader:
        (filename_without_extension, angle, ul_lat, ul_lon, ur_lat, ur_lon, ll_lat, ll_lon, 
        lr_lat, lr_lon, left_right_crop, up_down_crop) = row
        
        img = Image.open(os.path.join('datasets', input_folder, f"{filename_without_extension}.jpg"))
        img_rotated = img.rotate(float(angle), expand=True)
        
        # Cropping the image
        img_rotated = img_rotated.crop((int(left_right_crop), int(up_down_crop), 
                                        img_rotated.width - int(left_right_crop), 
                                        img_rotated.height - int(up_down_crop)))
        
        rotated_path = os.path.join('datasets', rotated_folder, f"rotated_{filename_without_extension}.jpg")
        img_rotated.save(rotated_path)
        
        width, height = img_rotated.size
        x_step = 256
        y_step = 256
        
        for x in range(0, width, x_step):
            for y in range(0, height, y_step):
                if x + x_step <= width and y + y_step <= height:  # Check to avoid border chunks
                    chunk = img_rotated.crop((x, y, x + x_step, y + y_step))
                    chunk_filename = f"{filename_without_extension}_{x}_{y}.jpg"
                    chunk_path = os.path.join('datasets', split_folder, chunk_filename)
                    chunk.save(chunk_path)

                    chunk_ul_lon, chunk_ul_lat, chunk_lr_lon, chunk_lr_lat = get_chunk_coordinates(x, y, width, height, float(ul_lon), float(ul_lat), float(lr_lon), float(lr_lat))
                    writer.writerow([chunk_filename, chunk_ul_lat, chunk_ul_lon, chunk_ul_lat, chunk_lr_lon, chunk_lr_lat, chunk_ul_lon, chunk_lr_lat, chunk_lr_lon])

print("Processing complete!")
