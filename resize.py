from PIL import Image
from PIL import Image

def resize_image(image_path):
  image = Image.open(image_path)
  max_size = 512
  width, height = image.size

  if width > height:
    new_width = max_size
    new_height = int(height * (max_size / width))
  else:
    new_height = max_size
    new_width = int(width * (max_size / height))

  resized_image = image.resize((new_width, new_height))
  resized_image.save(image_path)

resize_image("test.jpg")