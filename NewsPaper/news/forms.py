from django import forms
from .models import Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']

class SubscribeForm(forms.Form):
    subscribe = forms.BooleanField(required=False)