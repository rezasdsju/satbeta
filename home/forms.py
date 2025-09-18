from django import forms
from .models import UserPDF, PDFCategory

class UserPDFForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, 
        required=False, 
        label="Or create new category",
        widget=forms.TextInput(attrs={'placeholder': 'Enter new category name'})
    )
    
    class Meta:
        model = UserPDF
        fields = ['title', 'description', 'category', 'pdf_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['category'].queryset = PDFCategory.objects.all().order_by('name')
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        
        if not category and not new_category:
            raise forms.ValidationError("Please select a category or create a new one.")
        
        if category and new_category:
            raise forms.ValidationError("Please select either an existing category or create a new one, not both.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        new_category = self.cleaned_data.get('new_category')
        
        if new_category:
            category, created = PDFCategory.objects.get_or_create(
                name=new_category,
                defaults={'icon': 'fas fa-folder'}
            )
            instance.category = category
        
        if commit:
            instance.save()
        
        return instance