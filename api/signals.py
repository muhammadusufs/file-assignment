from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from api.models import UserFile
import os


@receiver(post_delete, sender=UserFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from storage
    when corresponding `UserFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(pre_save, sender=UserFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from storage
    when corresponding `UserFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = UserFile.objects.get(pk=instance.pk).file
    except UserFile.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
