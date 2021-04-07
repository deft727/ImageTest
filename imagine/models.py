from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse
from django.contrib.auth.models import User


class Image(models.Model):
    picture = ResizedImageField( upload_to='images/photos/%Y/%m/%d/',crop=['middle', 'center'],verbose_name='Картинка')

    def get_absolute_url(self):
        return reverse('image_detail',kwargs={'pk':self.pk})
    
    def __str__(self):
        return str(self.pk)


class Gallery(models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=150,verbose_name='Название ')
    owner =  models.ForeignKey('Profile', on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, blank=True )

    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk})
    
    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username