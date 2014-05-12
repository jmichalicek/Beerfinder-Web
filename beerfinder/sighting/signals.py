from .models import SightingImage
from django.db.models.signals import post_delete

def cleanup_sightingimage(sender, instance, **kwargs):
    obj.thumbnail.delete(save=False)
    obj.small.delete(save=False)
    obj.medium.delete(save=False)
    obj.original.delete(save=False)

post_delete.connect(cleanup_sightingimage, sender=SightingImage, dispatch_uid='cleanup_sightingimage_post_delete')
