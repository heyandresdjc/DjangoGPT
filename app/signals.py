from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import TrainingFile
from app.tasks import add_to_vector


@receiver(post_save, sender=TrainingFile)
def run_add_to_vector(sender, instance, created, **kwargs):
    if created:
        print("Run add")
        add_to_vector.delay(instance.pk)
