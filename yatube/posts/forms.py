from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        labels = {'text': 'Текст  поста', 'group': 'Группа'}
        widgets = {'text': forms.Textarea(attrs={'rows': 3})}



class SearchForm(forms.Form):
    query = forms.CharField()
