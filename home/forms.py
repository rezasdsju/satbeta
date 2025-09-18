from django import forms
from .models import UserPDF

class UserPDFForm(forms.ModelForm):
    class Meta:
        model = UserPDF
        fields = ['title', 'pdf_file']
