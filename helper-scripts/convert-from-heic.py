import os

import pyheif
from PIL import Image


def heic_to_jpeg(heic_path, jpeg_path):
    """Convert HEIC image to JPEG."""
    heif_file = pyheif.read(heic_path)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    image.save(jpeg_path, "JPEG")

def main(folder_path):
    """Convert all HEIC images in the folder to JPEG format."""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".heic"):
                file_path = os.path.join(root, file)
                jpeg_path = os.path.splitext(file_path)[0] + '.jpeg'
                heic_to_jpeg(file_path, jpeg_path)
                print(f"Converted: {file_path} to {jpeg_path}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing HEIC images: ")
    main(folder_path)
