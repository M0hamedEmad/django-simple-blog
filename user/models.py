from django.db import models
from django.contrib.auth.models import User
from PIL import Image

def upload_image(instance, filename):
    """ Change profile image to id of profile """

    _ , extention = filename.split('.')
    return f"user/{instance.id}.{extention}"

class Profile(models.Model):
    image = models.ImageField(default='user/default.jpg', upload_to=upload_image, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            img = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = img
        super().save(*args, **kwargs)


        img = Image.open(self.image.path)
        (width, height) = img.size
        if width > 800 and height > 800:
            img.thumbnail((800, 800))
            img.save(self.image.path) 