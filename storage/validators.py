from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def thumbnail_image_restriction(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width >= 300 or image_height >= 110:
        raise ValidationError('Image width needs to be less than 270px and height less than 100px')