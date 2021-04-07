from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from PIL import Image

def rename_image(instance, filename):
    """Change a image name to post id"""
    _ , extention = filename.split('.')
    return f"posts/{instance.id}.{extention}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='post')
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    categories = models.ManyToManyField(Category, blank=True, help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.')
    photo = models.ImageField(default='posts/default.jpg', upload_to=rename_image)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ make a slug to post, rename a image and resize a big image """
        # Handle a problem when rename a image 
        if self.pk is None:
            image = self.photo
            self.photo = None
            super().save(*args, **kwargs)
            self.photo = image            

        # make a slug before save a post
        post_slug = slugify(self.title)
        self.slug = f"{post_slug}_{self.id}"

        super().save(*args, **kwargs)

        # Resize a image
        img = Image.open(self.photo.path)
        if img.width > 800 or img.height > 800:
            img.thumbnail((800, 800))
            img.save(self.photo.path)

        

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80, null=True)
    content = models.TextField(max_length=700)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content   
