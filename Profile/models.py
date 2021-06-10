from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
import datetime

User = get_user_model()

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    likes = models.PositiveIntegerField(default=0, blank=True, null=True)

class PostWall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    des = models.CharField(max_length=256)
    image = models.ImageField(upload_to='post', blank=True, null=True, default='')
    like = models.ManyToManyField(LikePost, blank=True, default=1)
    date = models.DateField("Date", default=datetime.date.today)
    editMode = models.BooleanField(default=False)
    reviews = models.ManyToManyField('Reviews')
    def __str__(self):
        return str(self.des)
    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
        im = Image.open(self.image)
        im.save(self.image.path, optimize=True, quality=60)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(PostWall, self).delete(*args, **kwargs)

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='Родительский комментарий', blank=True, null=True,
                               related_name='comment_children', on_delete=models.CASCADE)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='reviews', null=True, blank=True)
    def __str__(self):
        return str(self.text)
