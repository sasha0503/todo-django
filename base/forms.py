from django.forms import ModelForm
from django import forms

from base.models import Task


class CreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control title-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 246px; height: 70px;',
                                                 'placeholder': '(не обов\'язково)'}),
        }


class UpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control title-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 246px; height: 70px;'}),
        }
