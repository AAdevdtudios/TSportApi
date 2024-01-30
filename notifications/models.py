from django.db import models
from django.conf import settings

# from tinymce import HTMLField


# Create your models here.
class Notifications(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=256)

    # content = HTMLField("Content")
    def save(self, *args, **kwargs):
        print(self.user)
        super(Notifications, self).save(*args, **kwargs)  # Call the real save() method
