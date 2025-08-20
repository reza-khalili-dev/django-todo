from django import forms
from .models import Task
from django.utils import timezone



class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),required=False)

    class Meta:
        model = Task
        fields = ['title','description','is_completed','priority','due_date']
        
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError('The date of entry cannot be in the past.')
        return due_date        