from PIL import Image
import os

# Folder containing images
input_folder = "images/"
output_folder = "webp_images/"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Convert all JPG and PNG files to WebP
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        webp_path = os.path.join(output_folder, filename.rsplit(".", 1)[0] + ".webp")
        
        # Save as WebP with compression
        img.save(webp_path, "WEBP", quality=80)  # Adjust quality if needed
        print(f"Converted: {filename} → {webp_path}")

print("✅ All images converted to WebP!")
    