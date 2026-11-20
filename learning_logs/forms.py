from django import forms

from .models import Entry, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Например: Шахматы, Python, Право…',
                'autofocus': True,
            }),
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Что вы узнали сегодня?',
                'autofocus': True,
            }),
        }
