from django import forms
from .models import Tasks

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'excerpt', 'image', 'due_date', 'content', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        complete_task = forms.BooleanField(
        required=False,  # The field is not required
        widget=forms.HiddenInput(),  # Hidden input field
    )