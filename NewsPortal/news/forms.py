from django import forms
from django.forms import ModelForm

from .models import Post, User, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categoryType',
            'title',
            'text',
            'postCategory',
        ]


class AuthorForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  ]


class SubscribeForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name']
