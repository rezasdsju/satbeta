from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    total_marks = models.FloatField(default=10.0)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"




class ResultSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    subjects = models.TextField()  # JSON string of subject data
    overall_gpa = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student_name} - {self.semester}"      
    
"""
class UserPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='user_pdfs/')  # MEDIA_ROOT/user_pdfs/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
"""

"""
# home/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserPDF(models.Model):
    CATEGORY_CHOICES = [
        ('statistics', 'Statistics and Data Science'),
        ('physics', 'HSC Physics'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='statistics')
    pdf_file = models.FileField(
        upload_to='user_pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
"""



from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class PDFCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(max_length=50, default='fas fa-folder')
    
    class Meta:
        verbose_name_plural = "PDF Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class UserPDF(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(PDFCategory, on_delete=models.SET_NULL, null=True, blank=True)
    pdf_file = models.FileField(
        upload_to='user_pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

   