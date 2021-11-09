from django.db import models
from django.utils import timezone
from account.models import CustomUser
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=30)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ["category_name"]

    def __str__(self):
        return self.category_name


class HashTag(models.Model):
    hashtag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.hashtag_name


class Blog(models.Model):
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    body = models.TextField()
    hashtag = models.ManyToManyField(HashTag)
    like = models.ManyToManyField(CustomUser, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:70]


class Comment(models.Model):
    post = models.ForeignKey(
        Blog, related_name="comments", on_delete=models.CASCADE)
    author_name = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    comment_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def approve(self):
        self.save()

    def __str__(self):
        return self.comment_text
