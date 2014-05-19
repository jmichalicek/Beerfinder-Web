from .models import SightingImage
from django.db.models.signals import post_delete

def cleanup_sightingimage(sender, instance, **kwargs):
    instance.thumbnail.delete(save=False)
    instance.small.delete(save=False)
    instance.medium.delete(save=False)
    instance.original.delete(save=False)

post_delete.connect(cleanup_sightingimage, sender=SightingImage, dispatch_uid='cleanup_sightingimage_post_delete')
