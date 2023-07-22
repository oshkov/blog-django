from .models import Posts
from django.forms import ModelForm, TextInput, Textarea

class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'text']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название записи'
            }),

            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст',
                'rows': '18',
                'style': 'resize: none'
            })
        }