import os 
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Animes, Episode



@receiver(post_delete, sender=Episode)
def delete_episode_video(sender, instance, **kwargs):
    if instance.video and os.path.isfile(instance.video.path):
        os.remove(instance.video.path)
@receiver(pre_save, sender=Episode)
def delete_old_episode_video(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Episode.objects.get(pk = instance.pk)
    except Episode.DoesNotExist:
        return
    

    old_video = old_instance.video
    new_video = instance.video

    if old_video and old_video != new_video:
        if os.path.isfile(old_video.path):
            os.remove(old_video.path)


@receiver(post_delete, sender=Animes)
def delete_anime_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(pre_save, sender=Animes)
def delete_old_anime_image(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Animes.objects.get(pk = instance.pk)
    except Animes.DoesNotExist:
        return
    
    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)