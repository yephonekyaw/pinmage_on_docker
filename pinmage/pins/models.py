from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse
from django.db import models

class Pin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='pin_created', 
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    # url = models.URLField(max_length=2000, null=True, blank=True)
    pin = models.ImageField(upload_to='images/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    users_saved = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='saved_pins',
                                        blank=True)       

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pins:pins_detail', args=[self.id, self.slug])


class Comment(models.Model):
    user = models.ForeignKey('auth.User', 
                            related_name='comments_on_pins',
                            on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin,
                            related_name='comments',
                            on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created'])
        ]
        ordering = ['created']

