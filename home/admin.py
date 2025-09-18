
from django.contrib import admin
#from .models import Student, Exam, ResultSheet
from .models import Student, Exam, ResultSheet, UserPDF

admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(ResultSheet)
admin.site.register(UserPDF)

