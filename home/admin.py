"""
from django.contrib import admin
#from .models import Student, Exam, ResultSheet
from .models import Student, Exam, ResultSheet, UserPDF

admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(ResultSheet)
admin.site.register(UserPDF)  """

from django.contrib import admin
from .models import Student, Exam, ResultSheet, UserPDF, PDFCategory

admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(ResultSheet)

@admin.register(PDFCategory)
class PDFCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(UserPDF)
class UserPDFAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'upload_date', 'is_approved')
    list_filter = ('is_approved', 'category', 'upload_date')
    search_fields = ('title', 'user__username', 'description')
    actions = ['approve_pdfs', 'disapprove_pdfs']
    
    def approve_pdfs(self, request, queryset):
        queryset.update(is_approved=True)
    approve_pdfs.short_description = "Approve selected PDFs"
    
    def disapprove_pdfs(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_pdfs.short_description = "Disapprove selected PDFs"

