from django import forms
from django.db import models
from django.forms import fields
from .models import Blog, Comment, Category


class BlogForm(forms.ModelForm):
    class Meta:  # 일종의 이름표 역할
        model = Blog
        fields = ['category', 'title', 'body', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
