"""
Generators for django-imagekit used in the sighting app
"""
import imagekit.exceptions

# Keeping these simple for now, but really will probably want more and/or different sizes
# particularly non-squares.  Images taken from my phone are about 1.77:1 ratio (1840x3264)
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, SmartResize, Thumbnail


class SightingImageThumbnail(ImageSpec):
    processors=[Thumbnail(150, 150)]
    format = 'JPEG'
    options = {'quality': 60}

class SightingImageSmall(ImageSpec):
    processors=[SmartResize(300, 300)]
    format = 'JPEG'
    options = {'quality': 80}

class SightingImageMedium(ImageSpec):
    processors = [SmartResize(750, 750)]
    format = 'JPEG'
    options = {'quality': 80}

#try:
register.generator('sighting:thumbnail', SightingImageThumbnail)
#except imagekit.exceptions.AlreadyRegistered:
#    pass

#try:
register.generator('sighting:small', SightingImageSmall)
#except imagekit.exceptions.AlreadyRegistered:
#    pass

#try:
register.generator('sighting:medium', SightingImageMedium)
#except imagekit.exceptions.AlreadyRegistered:
#    pass
