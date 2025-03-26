from django import forms
from .models import Comment, Post
from django_prose_editor.fields import ProseEditorFormField


class BlogPostForm(forms.ModelForm):
    body = ProseEditorFormField()
    class Meta:
        model = Post
        fields = ["title", "thumbnail", "status", "body"]

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()