import os
import cv2
import numpy as np
from PIL import Image, ExifTags
import random

def load_image_with_exif_orientation(path):
    img_pil = Image.open(path)

    # Handle EXIF orientation tag if present
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img_pil._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)

            if orientation_value == 3:
                img_pil = img_pil.rotate(180, expand=True)
            elif orientation_value == 6:
                img_pil = img_pil.rotate(270, expand=True)
            elif orientation_value == 8:
                img_pil = img_pil.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass  # no EXIF data or no orientation tag

    # Convert to OpenCV (BGR)
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return img_cv


# --- Settings ---
source_folder = "C:/tmp/photography"
# source_folder = "C:/tmp/photography/horilocal"

# output_folder = "C:/tmp/JLSwebsite/designbyjlswebsite/images/hori"  # your watermark image with transparency
output_folder = "C:/tmp/JLSwebsite/designbyjlswebsite/images/photography"  # your watermark image with transparency

watermark_path = "C:/tmp/JLSwebsite/designbyjlswebsite/images/DesignByJLS_Logo_v3.png"  # your watermark image with transparency
watermark = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)  # shape: (H, W, 4) or (H, W, 3)
# If no alpha channel, add one
if watermark.shape[2] == 3:
    b, g, r = cv2.split(watermark)
    alpha = np.ones_like(b, dtype=np.uint8) * 255  # fully opaque
    watermark = cv2.merge([b, g, r, alpha])
# Now watermark has 4 channels: B, G, R, A
b, g, r, a = cv2.split(watermark)
# Detect black pixels — you can adjust the tolerance if needed
black_mask = (r < 20) & (g < 20) & (b < 20)
# Set alpha to 0 for black pixels
a[black_mask] = 0
# Merge updated channels
watermark = cv2.merge([b, g, r, a])
scale_height_ratio = 0.06  # watermark height = 10% of image
padding = 10  # padding from edges
valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# Load watermark with alpha
# watermark = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)  # shape: (h, w, 4)
# if watermark is None or watermark.shape[2] != 4:
#     raise ValueError("Watermark image must have an alpha channel (PNG with transparency).")

html_lines = []

all_filenames = [
    f for f in os.listdir(source_folder)
    if os.path.splitext(f)[1].lower() in valid_extensions
]

random.shuffle(all_filenames)

for filename in all_filenames:
# for filename in sorted(os.listdir(source_folder)):
    print(f"Processing: {filename}")
    ext = os.path.splitext(filename)[1].lower()
    if ext not in valid_extensions:
        continue

    name, _ = os.path.splitext(filename)
    if ext == ".jpg" and ".jpg" in name.lower():
        # Remove the first occurrence of ".jpg" from the name
        new_name = name.lower().replace(".jpg", "", 1)
        new_filename = new_name + ext
        old_path = os.path.join(source_folder, filename)
        new_path = os.path.join(source_folder, new_filename)
        os.rename(old_path, new_path)
        filename = new_filename  # update filename for the rest of the loop

    input_path = os.path.join(source_folder, filename)
    output_path = os.path.join(output_folder, filename)

    # Load base image
    # image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    image = load_image_with_exif_orientation(input_path)
    if image is None:
        continue

    h_img, w_img = image.shape[:2]

    # Resize watermark to 10% of the smaller dimension (height or width)
    scale_ratio = min(h_img / watermark.shape[0], w_img / watermark.shape[1]) * 0.10
    wm_height = int(watermark.shape[0] * scale_ratio)
    wm_width = int(watermark.shape[1] * scale_ratio)
    wm_resized = cv2.resize(watermark, (wm_width, wm_height), interpolation=cv2.INTER_AREA)
    # wm_height = int(h_img * scale_height_ratio)
    # wm_ratio = watermark.shape[1] / watermark.shape[0]
    # wm_width = int(wm_height * wm_ratio)
    # wm_resized = cv2.resize(watermark, (wm_width, wm_height), interpolation=cv2.INTER_AREA)

    # Split watermark channels
    wm_bgr = wm_resized[:, :, :3]
    wm_alpha = wm_resized[:, :, 3] / 255.0  # Normalize to [0, 1]

    opacity_scale = 0.3  # adjust between 0 (invisible) to 1.0 (fully opaque)
    wm_alpha = (wm_resized[:, :, 3] / 255.0) * opacity_scale

    # Region of Interest (bottom-right)
    x_start = w_img - wm_width - padding
    y_start = h_img - wm_height - padding
    x_end = x_start + wm_width
    y_end = y_start + wm_height

    # Check bounds
    if x_start < 0 or y_start < 0:
        continue  # watermark too big for image

    roi = image[y_start:y_end, x_start:x_end]

    # Blend watermark onto ROI
    if roi.shape[:2] != wm_bgr.shape[:2]:
        continue  # shape mismatch, skip

    blended = (
        roi * (1 - wm_alpha[..., None]) + wm_bgr * wm_alpha[..., None]
    ).astype(np.uint8)
    image[y_start:y_end, x_start:x_end] = blended

    # Save result
    cv2.imwrite(output_path, image)

    # Generate HTML
    web_path = os.path.join("images", "photography", filename).replace("\\", "/")
    alt_text = os.path.splitext(filename)[0]
    # html = f'''    <div class="overlay-container">
    #   <img src="{web_path}" alt="{alt_text}" class="gallery-img" onclick="openModal(this.src)">
    # </div>'''

    html = f'''<div class="overlay-container">
      <img src="{web_path}" alt="Gallery 1" class="gallery-img" onclick="openModal(this.src)">
    </div>'''

    html_lines.append(html)



# Output HTML block
output_html = "\n".join(html_lines)
# print(output_html)

# Optional: write to file
with open("C:/tmp/gallery_output.html", "w") as f:
    f.write(output_html)

