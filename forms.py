from django import forms
from to_do.models import Todo

class Formtodo(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','task','completed']