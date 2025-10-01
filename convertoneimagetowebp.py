from PIL import Image
import os

# Folder containing images
theproj = "corn"
filename = "corn_img_0_.png"
# input_file = "C:/tmp/" + theproj + "/" + filename
input_file = "G:/My Drive/Design/DesignPersonal/DesignByJLS/StereogramStuff/" + filename
output_folder = "C:/tmp/JLSwebsite/designbyjlswebsite/images/"

# Convert the specified file to WebP, resize, and place in the output folder
input_folder = os.path.dirname(input_file)
img = Image.open(input_file)

# Resize image (example: max width 800px, maintain aspect ratio)
max_width = 216
if img.width > max_width:
    w_percent = (max_width / float(img.width))
    h_size = int((float(img.height) * float(w_percent)))
    img = img.resize((max_width, h_size), Image.LANCZOS)

webp_filename = theproj + "THUMB.webp"
webp_path = os.path.join(output_folder, webp_filename)
img.save(webp_path, "WEBP", quality=80)
print(f"Converted and resized: {input_file} → {webp_path}")


    