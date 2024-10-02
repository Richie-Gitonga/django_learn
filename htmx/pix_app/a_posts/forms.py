from django.forms import ModelForm
from django import forms
from .models import Post, Comments


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {
            'body': 'Caption',
            'tags': 'Category'
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption ...', 'class': 'font1 text-2xl'}),
            'url': forms.TextInput(attrs={'placeholder': 'Add url ...'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {
            'body': '',
            'tags': 'Category'
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption ...', 'class': 'font1 text-2xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a comment ...'}),
        }
