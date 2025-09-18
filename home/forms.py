# home/forms.py
from django import forms
from .models import UserPDF

class UserPDFForm(forms.ModelForm):
    class Meta:
        model = UserPDF
        fields = ['title', 'description', 'category', 'pdf_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }