#home/views.py======================================
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core import serializers          
import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from .models import Student, Exam, ResultSheet
from django.utils import timezone









from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserPDFForm
from .models import UserPDF

def index(request):
    return render(request, 'home/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def programming_hub_view(request):
    return render(request, 'home/programming/program_hub.html')
def python_child_1_view(request):
    return render(request, "home/programming/python_child_1.html")

def python_runner(request):
    return render(request, "home/programming/python_runner_0.html")
def django_minor_details_view(request):
    return render(request, 'home/programming/djn_minor_details.html')
def user_auth_tutorial_view(request):
    return render(request, "home/programming/user_auth.html")
def ban_ara_eng_layout(request):
    return render(request,'home/programming/latex/layout_1.html')
def tutorials_hub_view(request):
    return render(request, 'home/tutorials/tutorial_hub.html')
def conf_matrix_view(request):
    return render(request, 'home/tutorials/conf_matrix.html')
"""
def pdf_hub_view(request):
    return render(request, 'home/pdf/pdf_hub.html')"""
"""
def pdf_hub_view(request):
    # শুধু approved PDFs দেখাবে
    pdfs = UserPDF.objects.filter(is_approved=True)
    return render(request, 'home/pdf/pdf_hub.html', {'pdfs': pdfs})
def vector_pdf_view(request):
    return render(request, 'home/pdf/vec_pdf.html')










@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = UserPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user
            pdf.save()
            return redirect('pdf_hub')
    else:
        form = UserPDFForm()
    return render(request, 'home/pdf/upload_pdf.html', {'form': form})
"""
"""
def pdf_hub(request):
    pdfs = UserPDF.objects.all()
    return render(request, 'home/pdf/pdf_hub.html', {'pdfs': pdfs})"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserPDFForm
from .models import UserPDF, PDFCategory

def pdf_hub_view(request):
    # শুধু approved PDFs দেখাবে, ক্যাটাগরি অনুসারে গ্রুপ করে
    categories = PDFCategory.objects.all().prefetch_related('userpdf_set')
    
    # User uploaded PDFs (approved ones)
    user_pdfs = UserPDF.objects.filter(is_approved=True)
    
    return render(request, 'home/pdf/pdf_hub.html', {
        'categories': categories,
        'user_pdfs': user_pdfs
    })

def vector_pdf_view(request):
    return render(request, 'home/pdf/vec_pdf.html')

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = UserPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user
            pdf.save()
            return redirect('pdf_hub')
    else:
        form = UserPDFForm()
    
    return render(request, 'home/pdf/upload_pdf.html', {'form': form})


def result_for_view(request):
    return render(request, 'home/result/result_for.html')

# New result system views
@login_required
def school_mark_input(request):
    """Render the input form for school marks"""
    # Get all saved results for the current user
    user_results = ResultSheet.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'home/result/school_mark_input.html', {
        'user_results': user_results
    })

"""
@login_required
def show_school_result(request):
    #Process the form data and display the result 
    if request.method == 'POST':
        # Get form data
        student_name = request.POST.get('student-name')
        semester = request.POST.get('semester')
        
        # Get subjects data (arrays from form)
        subjects = request.POST.getlist('subject[]')
        marks = request.POST.getlist('mark[]')
        full_marks = request.POST.getlist('fullMark[]')
        
        # Process each subject
        subject_data = []
        total_gpa_points = 0
        subject_count = 0
        has_failed = False
        
        for i in range(len(subjects)):
            if subjects[i] and marks[i]:
                mark = float(marks[i])
                full_mark = float(full_marks[i])
                
                # Calculate grade and GPA
                grade, gpa = calculate_grade_and_gpa(mark, full_mark)
                
                subject_data.append({
                    'name': subjects[i],
                    'mark': mark,
                    'sub_full_mark': full_mark,
                    'semester': semester,
                    'grade': grade,
                    'gpa': gpa
                })
                
                total_gpa_points += gpa
                subject_count += 1
                
                if grade == 'F':
                    has_failed = True
        
        # Calculate overall GPA
        if subject_count > 0:
            overall_gpa = 0.00 if has_failed else round(total_gpa_points / subject_count, 2)
        else:
            overall_gpa = 0.00
        
        # Save to database
        result_sheet = ResultSheet(
            user=request.user,
            student_name=student_name,
            semester=semester,
            subjects=json.dumps(subject_data),
            overall_gpa=overall_gpa
        )
        result_sheet.save()
        
        # Get all results for this user to display
        all_results = ResultSheet.objects.filter(user=request.user).order_by('-created_at')
        
        context = {
            'student_name': student_name,
            'semester': semester,
            'subjects': subject_data,
            'overall_gpa': overall_gpa,
            'result_id': result_sheet.id,
            'all_results': all_results
        }
        
        return render(request, 'home/result/show_school_result.html', context)
    
    # If not POST, redirect to input form
    return redirect('school_mark_input') 

    """ 
















@login_required
def show_school_result(request):
    """Process the form data and display the result"""
    if request.method == 'POST':
        # Get form data
        student_name = request.POST.get('student-name')
        semester = request.POST.get('semester')
        
        # Get subjects data (arrays from form)
        subjects = request.POST.getlist('subject[]')
        marks = request.POST.getlist('mark[]')
        full_marks = request.POST.getlist('fullMark[]')
        
        # Process each subject
        subject_data = []
        total_gpa_points = 0
        subject_count = 0
        has_failed = False
        
        for i in range(len(subjects)):
            if subjects[i] and marks[i]:
                mark = float(marks[i])
                full_mark = float(full_marks[i])
                
                # Calculate grade and GPA
                grade, gpa = calculate_grade_and_gpa(mark, full_mark)
                
                subject_data.append({
                    'name': subjects[i],
                    'mark': mark,
                    'sub_full_mark': full_mark,
                    'semester': semester,
                    'grade': grade,
                    'gpa': gpa
                })
                
                total_gpa_points += gpa
                subject_count += 1
                
                if grade == 'F':
                    has_failed = True
        
        # Calculate overall GPA
        if subject_count > 0:
            overall_gpa = 0.00 if has_failed else round(total_gpa_points / subject_count, 2)
        else:
            overall_gpa = 0.00
        
        # Save to database
        result_sheet = ResultSheet(
            user=request.user,
            student_name=student_name,
            semester=semester,
            subjects=json.dumps(subject_data),
            overall_gpa=overall_gpa
        )
        result_sheet.save()
    
    # Get all results for this user to display (both for POST and GET requests)
    all_results = ResultSheet.objects.filter(user=request.user).order_by('-created_at')
    
    # Prepare results with parsed subjects
    results_with_subjects = []
    for result in all_results:
        results_with_subjects.append({
            'id': result.id,
            'student_name': result.student_name,
            'semester': result.semester,
            'overall_gpa': result.overall_gpa,
            'created_at': result.created_at,
            'subjects_list': json.loads(result.subjects)
        })
    
    context = {
        'all_results': results_with_subjects
    }
    
    return render(request, 'home/result/show_school_result.html', context)



























@login_required
def download_single_csv(request, result_id):
    """Download a single result sheet as CSV"""
    try:
        result_sheet = ResultSheet.objects.get(id=result_id, user=request.user)
        subjects = json.loads(result_sheet.subjects)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{result_sheet.student_name}_result.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student Name', result_sheet.student_name])
        writer.writerow(['Semester', result_sheet.semester])
        writer.writerow(['Overall GPA', result_sheet.overall_gpa])
        writer.writerow([])
        writer.writerow(['Subject', 'Mark', 'Full Mark', 'Grade', 'GPA'])
        
        for subject in subjects:
            writer.writerow([
                subject['name'],
                subject['mark'],
                subject['sub_full_mark'],
                subject['grade'],
                subject['gpa']
            ])
            
        return response
    except ResultSheet.DoesNotExist:
        return HttpResponse("Result not found", status=404)
"""
@login_required
def download_single_pdf(request, result_id):
    #Download a single result sheet as PDF
    try:
        result_sheet = ResultSheet.objects.get(id=result_id, user=request.user)
        subjects = json.loads(result_sheet.subjects)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{result_sheet.student_name}_result.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"Result Sheet for {result_sheet.student_name}", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Semester: {result_sheet.semester}", styles['Normal']))
        elements.append(Paragraph(f"Overall GPA: {result_sheet.overall_gpa}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Create table data
        table_data = [['Subject', 'Mark', 'Full Mark', 'Grade', 'GPA']]
        for subject in subjects:
            table_data.append([
                subject['name'],
                str(subject['mark']),
                str(subject['sub_full_mark']),
                subject['grade'],
                str(subject['gpa'])
            ])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        return response
    except ResultSheet.DoesNotExist:
        return HttpResponse("Result not found", status=404)"""


from reportlab.lib.styles import ParagraphStyle

@login_required
def download_single_pdf(request, result_id):
    """Download a single result sheet as PDF"""
    try:
        result_sheet = ResultSheet.objects.get(id=result_id, user=request.user)
        subjects = json.loads(result_sheet.subjects)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{result_sheet.student_name}_result.pdf"'
        
        # Set page margins
        doc = SimpleDocTemplate(response, pagesize=letter, 
                                leftMargin=40, rightMargin=40, 
                                topMargin=40, bottomMargin=40)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom style for "RESULT SHEET" heading
        result_sheet_style = ParagraphStyle(
            'ResultSheetStyle',
            parent=styles['Title'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),  # Dark blue color
            spaceAfter=25,
            alignment=1,  # Center alignment
            fontName='Helvetica-Bold'
        )
        
        # Custom style for student name
        student_name_style = ParagraphStyle(
            'StudentNameStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#2980b9'),  # Blue color
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        # Custom style for semester
        semester_style = ParagraphStyle(
            'SemesterStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#0000FF'),  # Dark blue-gray color
            spaceAfter=8
        )
        
        # Custom style for overall GPA
        gpa_style = ParagraphStyle(
            'GPAStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#27ae60'),  # Green color
            spaceAfter=25,
            fontName='Helvetica-Bold'
        )
        
        # Title with custom styling
        elements.append(Paragraph(f"RESULT SHEET", result_sheet_style))
        
        # Student info with custom styling
        elements.append(Paragraph(f"Student Name: {result_sheet.student_name}", student_name_style))
        elements.append(Paragraph(f"Semester: {result_sheet.semester}", semester_style))
        elements.append(Paragraph(f"Overall GPA: {result_sheet.overall_gpa}", gpa_style))
        elements.append(Spacer(1, 25))
        
        # Create table data
        table_data = [['Subject', 'Mark', 'Full Mark', 'Grade', 'GPA']]
        for subject in subjects:
            table_data.append([
                subject['name'],
                str(subject['mark']),
                str(subject['sub_full_mark']),
                subject['grade'],
                str(subject['gpa'])
            ])
        
        # Create table with better styling
        table = Table(table_data, colWidths=[200, 60, 60, 60, 60])
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#43cbff')),  # Light blue
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),  # Light gray
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#495057')),   # Dark gray
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),  # Light gray border
            
            # Highlight failed subjects (grade F)
            ('TEXTCOLOR', (0, 1), (-1, -1), 
                lambda row, col, table=table_data: 
                colors.red if row > 0 and table[row][3] == 'F' else colors.HexColor('#495057')),
            
            # First column alignment (subject names)
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (0, -1), 10),
            
            # Row height
            ('LEADING', (0, 0), (-1, -1), 14),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Add footer with date
        footer_style = styles['Normal']
        footer_style.fontSize = 10
        footer_style.textColor = colors.HexColor('#6c757d')  # Gray color
        #elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y %I:%M %p')}", footer_style))
        
        doc.build(elements)
        
        return response
    except ResultSheet.DoesNotExist:
        return HttpResponse("Result not found", status=404)










@login_required
def download_all_csv(request):
    """Download all result sheets as a single CSV"""
    result_sheets = ResultSheet.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_results.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['All Result Sheets'])
    writer.writerow([])
    
    for result_sheet in result_sheets:
        subjects = json.loads(result_sheet.subjects)
        
        writer.writerow(['Student Name', result_sheet.student_name])
        writer.writerow(['Semester', result_sheet.semester])
        writer.writerow(['Overall GPA', result_sheet.overall_gpa])
        writer.writerow(['Subject', 'Mark', 'Full Mark', 'Grade', 'GPA'])
        
        for subject in subjects:
            writer.writerow([
                subject['name'],
                subject['mark'],
                subject['sub_full_mark'],
                subject['grade'],
                subject['gpa']
            ])
            
        writer.writerow([])
        writer.writerow([])
            
    return response


"""
@login_required
def download_all_pdf(request):
    #Download all result sheets as a single PDF
    result_sheets = ResultSheet.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_results.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    
    for result_sheet in result_sheets:
        subjects = json.loads(result_sheet.subjects)
        
        elements.append(Paragraph(f"Result Sheet for {result_sheet.student_name}", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Semester: {result_sheet.semester}", styles['Normal']))
        elements.append(Paragraph(f"Overall GPA: {result_sheet.overall_gpa}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Create table data
        table_data = [['Subject', 'Mark', 'Full Mark', 'Grade', 'GPA']]
        for subject in subjects:
            table_data.append([
                subject['name'],
                str(subject['mark']),
                str(subject['sub_full_mark']),
                subject['grade'],
                str(subject['gpa'])
            ])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 40))
    
    doc.build(elements)
    
    return response"""


@login_required
def download_all_pdf(request):
    """Download all result sheets as a single PDF"""
    result_sheets = ResultSheet.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_results.pdf"'
    
    # Set page margins
    doc = SimpleDocTemplate(response, pagesize=letter, 
                            leftMargin=40, rightMargin=40, 
                            topMargin=40, bottomMargin=40)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Main title for the document
    main_title_style = styles['Title']
    main_title_style.textColor = colors.HexColor('#2c3e50')
    main_title_style.fontSize = 20
    main_title_style.spaceAfter = 30
    main_title_style.alignment = 1  # Center alignment
    elements.append(Paragraph("ALL RESULT SHEETS", main_title_style))
    
    for result_sheet in result_sheets:
        subjects = json.loads(result_sheet.subjects)
        
        # Individual result header with better styling
        header_style = styles['Heading1']
        header_style.textColor = colors.HexColor('#43cbff')  # Light blue
        header_style.fontSize = 16
        header_style.spaceAfter = 12
        elements.append(Paragraph(f"RESULT SHEET FOR {result_sheet.student_name.upper()}", header_style))
        
        # Student info with better styling
        info_style = styles['Normal']
        info_style.fontSize = 12
        info_style.spaceAfter = 6
        info_style.textColor = colors.HexColor('#4a6491')  # Dark blue
        
        # Create a custom style for highlighted info
        highlight_style = styles['Normal']
        highlight_style.fontSize = 12
        highlight_style.textColor = colors.HexColor('#9708cc')  # Purple
        highlight_style.fontName = 'Helvetica-Bold'
        
        elements.append(Paragraph(f"<b>Student Name:</b> <font color='#9708cc'>{result_sheet.student_name}</font>", info_style))
        elements.append(Paragraph(f"<b>Semester:</b> <font color='#9708cc'>{result_sheet.semester}</font>", info_style))
        elements.append(Paragraph(f"<b>Overall GPA:</b> <font color='#9708cc'>{result_sheet.overall_gpa}</font>", info_style))
        elements.append(Spacer(1, 20))
        
        # Create table data
        table_data = [['Subject', 'Mark', 'Full Mark', 'Grade', 'GPA']]
        for subject in subjects:
            table_data.append([
                subject['name'],
                str(subject['mark']),
                str(subject['sub_full_mark']),
                subject['grade'],
                str(subject['gpa'])
            ])
        
        # Create table with better styling
        table = Table(table_data, colWidths=[200, 60, 60, 60, 60])
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#43cbff')),  # Light blue
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),  # Light gray
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#495057')),   # Dark gray
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),  # Light gray border
            
            # Highlight failed subjects (grade F)
            ('TEXTCOLOR', (0, 1), (-1, -1), 
                lambda row, col, table=table_data: 
                colors.red if row > 0 and table[row][3] == 'F' else colors.HexColor('#495057')),
            
            # First column alignment (subject names)
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (0, -1), 10),
            
            # Row height
            ('LEADING', (0, 0), (-1, -1), 14),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        # Add a separator line between result sheets
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<hr/>", styles['Normal']))
        elements.append(Spacer(1, 20))
    
    # Add footer with generation date
    footer_style = styles['Normal']
    footer_style.fontSize = 10
    footer_style.textColor = colors.HexColor('#6c757d')  # Gray color
    footer_style.alignment = 1  # Center alignment
    elements.append(Spacer(1, 20))
    #elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y %I:%M %p')}", footer_style))
    
    doc.build(elements)
    
    return response









     

@login_required
def clear_all_results(request):
    """Clear all result sheets for the current user"""
    if request.method == 'POST':
        ResultSheet.objects.filter(user=request.user).delete()
        return redirect('school_mark_input')
    return redirect('school_mark_input')

def calculate_grade_and_gpa(mark, full_mark):
    """Calculate grade and GPA based on mark and full mark"""
    if full_mark == 100:
        if mark >= 80: return 'A+', 5.00
        elif mark >= 70: return 'A', 4.00
        elif mark >= 60: return 'A-', 3.50
        elif mark >= 50: return 'B', 3.00
        elif mark >= 40: return 'C', 2.00
        elif mark >= 33: return 'D', 1.00
        else: return 'F', 0.00
    elif full_mark == 50:
        if mark >= 40: return 'A+', 5.00
        elif mark >= 35: return 'A', 4.00
        elif mark >= 30: return 'A-', 3.50
        elif mark >= 25: return 'B', 3.00
        elif mark >= 20: return 'C', 2.00
        elif mark >= 17: return 'D', 1.00
        else: return 'F', 0.00
    elif full_mark == 200:
        if mark >= 160: return 'A+', 5.00
        elif mark >= 140: return 'A', 4.00
        elif mark >= 120: return 'A-', 3.50
        elif mark >= 100: return 'B', 3.00
        elif mark >= 80: return 'C', 2.00
        elif mark >= 66: return 'D', 1.00
        else: return 'F', 0.00
    else:
        return 'F', 0.00      


@login_required
def varsity_mark_input(request):
    """Render the input form for university marks"""
    # Get all saved results for the current user
    user_results = ResultSheet.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'home/result/varsity_mark_input.html', {
        'user_results': user_results
    })

@login_required
def show_varsity_result(request):
    """Process the form data and display the result"""
    if request.method == 'POST':
        # Get form data
        student_name = request.POST.get('student-name')
        semester = request.POST.get('semester')
        
        # Get subjects data (arrays from form)
        subjects = request.POST.getlist('subject[]')
        marks = request.POST.getlist('mark[]')
        credits = request.POST.getlist('credit[]')
        full_marks = request.POST.getlist('fullMark[]')
        
        # Process each subject
        subject_data = []
        total_gpa_points = 0
        total_credits = 0
        has_failed = False
        
        for i in range(len(subjects)):
            if subjects[i] and marks[i]:
                mark = float(marks[i])
                credit = float(credits[i])
                full_mark = float(full_marks[i])
                
                # Calculate grade and GPA
                grade, gpa = varsity_calculate_grade_and_gpa(mark, full_mark)
                
                subject_data.append({
                    'name': subjects[i],
                    'mark': mark,
                    'sub_full_mark': full_mark,
                    'credit': credit,
                    'grade': grade,
                    'gpa': gpa
                })
                
                total_gpa_points += gpa * credit
                total_credits += credit
                
                if grade == 'F':
                    has_failed = True
        
        # Calculate overall GPA
        if total_credits > 0:
            overall_gpa = 0.00 if has_failed else round(total_gpa_points / total_credits, 2)
        else:
            overall_gpa = 0.00
        
        # Save to database
        result_sheet = ResultSheet(
            user=request.user,
            student_name=student_name,
            semester=semester,
            subjects=json.dumps(subject_data),
            overall_gpa=overall_gpa
        )
        result_sheet.save()
    
    # Get all results for this user to display (both for POST and GET requests)
    all_results = ResultSheet.objects.filter(user=request.user).order_by('-created_at')
    
    # Prepare results with parsed subjects
    results_with_subjects = []
    for result in all_results:
        results_with_subjects.append({
            'id': result.id,
            'student_name': result.student_name,
            'semester': result.semester,
            'overall_gpa': result.overall_gpa,
            'created_at': result.created_at,
            'subjects_list': json.loads(result.subjects)
        })
    
    context = {
        'all_results': results_with_subjects
    }
    
    return render(request, 'home/result/show_varsity_result.html', context)

def varsity_download_single_csv(request, result_id):
    """Download a single result sheet as CSV"""
    try:
        result_sheet = ResultSheet.objects.get(id=result_id, user=request.user)
        subjects = json.loads(result_sheet.subjects)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{result_sheet.student_name}_result.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student Name', result_sheet.student_name])
        writer.writerow(['Semester', result_sheet.semester])
        writer.writerow(['Overall GPA', result_sheet.overall_gpa])
        writer.writerow([])
        writer.writerow(['Subject', 'Mark', 'Full Mark', 'Credit', 'Grade', 'GPA'])
        
        for subject in subjects:
            writer.writerow([
                subject['name'],
                subject['mark'],
                subject['sub_full_mark'],
                subject['credit'],
                subject['grade'],
                subject['gpa']
            ])
            
        return response
    except ResultSheet.DoesNotExist:
        return HttpResponse("Result not found", status=404)

@login_required
def varsity_download_single_pdf(request, result_id):
    """Download a single result sheet as PDF"""
    try:
        result_sheet = ResultSheet.objects.get(id=result_id, user=request.user)
        subjects = json.loads(result_sheet.subjects)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{result_sheet.student_name}_result.pdf"'
        
        # Set page margins
        doc = SimpleDocTemplate(response, pagesize=letter, 
                                leftMargin=40, rightMargin=40, 
                                topMargin=40, bottomMargin=40)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom style for "RESULT SHEET" heading
        result_sheet_style = ParagraphStyle(
            'ResultSheetStyle',
            parent=styles['Title'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=25,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        # Custom style for student name
        student_name_style = ParagraphStyle(
            'StudentNameStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#2980b9'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        # Custom style for semester
        semester_style = ParagraphStyle(
            'SemesterStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#0000FF'),
            spaceAfter=8
        )
        
        # Custom style for overall GPA
        gpa_style = ParagraphStyle(
            'GPAStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#27ae60'),
            spaceAfter=25,
            fontName='Helvetica-Bold'
        )
        
        # Title with custom styling
        elements.append(Paragraph(f"RESULT SHEET", result_sheet_style))
        
        # Student info with custom styling
        elements.append(Paragraph(f"Student Name: {result_sheet.student_name}", student_name_style))
        elements.append(Paragraph(f"Semester: {result_sheet.semester}", semester_style))
        elements.append(Paragraph(f"Overall GPA: {result_sheet.overall_gpa}", gpa_style))
        elements.append(Spacer(1, 25))
        
        # Create table data
        table_data = [['Subject', 'Mark', 'Full Mark', 'Credit', 'Grade', 'GPA']]
        for subject in subjects:
            table_data.append([
                subject['name'],
                str(subject['mark']),
                str(subject['sub_full_mark']),
                str(subject['credit']),
                subject['grade'],
                str(subject['gpa'])
            ])
        
        # Create table with better styling
        table = Table(table_data, colWidths=[180, 50, 50, 50, 50, 50])
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#43cbff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#495057')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            
            # Highlight failed subjects (grade F)
            ('TEXTCOLOR', (0, 1), (-1, -1), 
                lambda row, col, table=table_data: 
                colors.red if row > 0 and table[row][4] == 'F' else colors.HexColor('#495057')),
            
            # First column alignment (subject names)
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (0, -1), 10),
            
            # Row height
            ('LEADING', (0, 0), (-1, -1), 14),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Add footer with date
        footer_style = styles['Normal']
        footer_style.fontSize = 10
        footer_style.textColor = colors.HexColor('#6c757d')
        elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y %I:%M %p')}", footer_style))
        
        doc.build(elements)
        
        return response
    except ResultSheet.DoesNotExist:
        return HttpResponse("Result not found", status=404)

@login_required
def varsity_download_all_csv(request):
    """Download all result sheets as a single CSV"""
    result_sheets = ResultSheet.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_results.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['All Result Sheets'])
    writer.writerow([])
    
    for result_sheet in result_sheets:
        subjects = json.loads(result_sheet.subjects)
        
        writer.writerow(['Student Name', result_sheet.student_name])
        writer.writerow(['Semester', result_sheet.semester])
        writer.writerow(['Overall GPA', result_sheet.overall_gpa])
        writer.writerow(['Subject', 'Mark', 'Full Mark', 'Credit', 'Grade', 'GPA'])
        
        for subject in subjects:
            writer.writerow([
                subject['name'],
                subject['mark'],
                subject['sub_full_mark'],
                subject['credit'],
                subject['grade'],
                subject['gpa']
            ])
            
        writer.writerow([])
        writer.writerow([])
            
    return response

@login_required
def varsity_download_all_pdf(request):
    """Download all result sheets as a single PDF"""
    result_sheets = ResultSheet.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_results.pdf"'
    
    # Set page margins
    doc = SimpleDocTemplate(response, pagesize=letter, 
                            leftMargin=40, rightMargin=40, 
                            topMargin=40, bottomMargin=40)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Main title for the document
    main_title_style = styles['Title']
    main_title_style.textColor = colors.HexColor('#2c3e50')
    main_title_style.fontSize = 20
    main_title_style.spaceAfter = 30
    main_title_style.alignment = 1
    elements.append(Paragraph("ALL RESULT SHEETS", main_title_style))
    
    for result_sheet in result_sheets:
        subjects = json.loads(result_sheet.subjects)
        
        # Individual result header with better styling
        header_style = styles['Heading1']
        header_style.textColor = colors.HexColor('#43cbff')
        header_style.fontSize = 16
        header_style.spaceAfter = 12
        elements.append(Paragraph(f"RESULT SHEET FOR {result_sheet.student_name.upper()}", header_style))
        
        # Student info with better styling
        info_style = styles['Normal']
        info_style.fontSize = 12
        info_style.spaceAfter = 6
        info_style.textColor = colors.HexColor('#4a6491')
        
        elements.append(Paragraph(f"<b>Student Name:</b> <font color='#9708cc'>{result_sheet.student_name}</font>", info_style))
        elements.append(Paragraph(f"<b>Semester:</b> <font color='#9708cc'>{result_sheet.semester}</font>", info_style))
        elements.append(Paragraph(f"<b>Overall GPA:</b> <font color='#9708cc'>{result_sheet.overall_gpa}</font>", info_style))
        elements.append(Spacer(1, 20))
        
        # Create table data
        table_data = [['Subject', 'Mark', 'Full Mark', 'Credit', 'Grade', 'GPA']]
        for subject in subjects:
            table_data.append([
                subject['name'],
                str(subject['mark']),
                str(subject['sub_full_mark']),
                str(subject['credit']),
                subject['grade'],
                str(subject['gpa'])
            ])
        
        # Create table with better styling
        table = Table(table_data, colWidths=[180, 50, 50, 50, 50, 50])
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#43cbff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#495057')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            
            # Highlight failed subjects (grade F)
            ('TEXTCOLOR', (0, 1), (-1, -1), 
                lambda row, col, table=table_data: 
                colors.red if row > 0 and table[row][4] == 'F' else colors.HexColor('#495057')),
            
            # First column alignment (subject names)
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (0, -1), 10),
            
            # Row height
            ('LEADING', (0, 0), (-1, -1), 14),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        # Add a separator line between result sheets
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<hr/>", styles['Normal']))
        elements.append(Spacer(1, 20))
    
    # Add footer with generation date
    footer_style = styles['Normal']
    footer_style.fontSize = 10
    footer_style.textColor = colors.HexColor('#6c757d')
    footer_style.alignment = 1
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%B %d, %Y %I:%M %p')}", footer_style))
    
    doc.build(elements)
    
    return response

@login_required
def varsity_clear_all_results(request):
    """Clear all result sheets for the current user"""
    if request.method == 'POST':
        ResultSheet.objects.filter(user=request.user).delete()
        return redirect('varsity_mark_input')
    return redirect('varsity_mark_input')

def varsity_calculate_grade_and_gpa(mark, full_mark):
    """Calculate grade and GPA based on mark and full mark"""
    if full_mark == 100:
        if mark >= 80: return 'A+', 4.00
        elif mark >= 75: return 'A', 3.75
        elif mark >= 70: return 'A-', 3.50
        elif mark >= 65: return 'B+', 3.25
        elif mark >= 60: return 'B', 3.00
        elif mark >= 55: return 'B-', 2.75
        elif mark >= 50: return 'C+', 2.50
        elif mark >= 45: return 'C', 2.25
        elif mark >= 40: return 'D', 2.00
        else: return 'F', 0.00
    elif full_mark == 50:
        if mark >= 40: return 'A+', 4.00
        elif mark >= 37.5: return 'A', 3.75
        elif mark >= 35: return 'A-', 3.50
        elif mark >= 32.5: return 'B+', 3.25
        elif mark >= 30: return 'B', 3.00
        elif mark >= 27.5: return 'B-', 2.75
        elif mark >= 25: return 'C+', 2.50
        elif mark >= 22.5: return 'C', 2.25
        elif mark >= 20: return 'D', 2.00
        else: return 'F', 0.00
    elif full_mark == 200:
        if mark >= 160: return 'A+', 4.00
        elif mark >= 150: return 'A', 3.75
        elif mark >= 140: return 'A-', 3.50
        elif mark >= 130: return 'B+', 3.25
        elif mark >= 120: return 'B', 3.00
        elif mark >= 110: return 'B-', 2.75
        elif mark >= 100: return 'C+', 2.50
        elif mark >= 90: return 'C', 2.25
        elif mark >= 80: return 'D', 2.00
        else: return 'F', 0.00
    else:
        return 'F', 0.00      


def mcq_hub_view(request):
    return render(request, 'home/mcq/mcq_hub.html')

def narration_view(request):
    return render(request, 'home/mcq/narration.html')

def vocabulary_view(request): 
    return render(request, 'home/mcq/vocab_main.html')

def bcs_english_view(request):
    return render(request, 'home/mcq/bcs_english.html')
def vector_mcq_view(request):
    return render(request, 'home/mcq/vector_main_mcq.html')





@require_POST
@csrf_exempt
def submit_exam(request):
    if request.method == "POST":
        # Check if it's AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Form data থেকে name এবং score নিন
            name = request.POST.get("studentName")
            score = request.POST.get("score")
            total = request.POST.get("total", 10)
            
            subject = request.POST.get("subject")  # ডিফল্ট রাখুন

            # যদি subject ফাঁকা থাকে, fallback দিন
            if not subject:
                subject = "General"
            
            # Student create or get
            student, created = Student.objects.get_or_create(
                name=name, 
                defaults={'email': f'{name.lower().replace(" ", "")}@example.com'}
            )
            
            # Exam save
            Exam.objects.create(
                student=student, 
                subject=subject, 
                score=float(score),
                total_marks=float(total)
            )
            
            return JsonResponse({'success': True})
        
        else:
            # Handle regular form submission (যদি form থাকে)
            return JsonResponse({'success': False, 'error': 'Invalid request type'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def ranking_view(request):
    # Subject এবং name filter করার জন্য
    subject = request.GET.get('subject', '')
    search_name = request.GET.get('search_name', '')
    
    # Calculate cumulative scores for each student
    from django.db.models import Sum, Min, Count
    cumulative_scores = Exam.objects.values('student__name', 'subject').annotate(
        total_score=Sum('score'),
        total_marks=Sum('total_marks'),
        first_exam_date=Min('date_taken'),
        number_of_exam=Count('id')
    )

    # Apply filters
    if subject:
        cumulative_scores = cumulative_scores.filter(subject=subject)
    
    # Calculate points for each student
    students_with_points = []
    for item in cumulative_scores:
        if item['total_marks'] and item['total_marks'] > 0:
            points = item['total_score'] 
        else:
            points = 0
            
        students_with_points.append({
            'name': item['student__name'],
            'subject': item['subject'],
            'points': round(points, 2),
            'total_score': item['total_score'],
            'total_marks': item['total_marks'],
            'first_exam_date': item['first_exam_date']
        })

    # Sort by points descending
    students_with_points.sort(key=lambda x: (-x['points'], x['first_exam_date']))

    # Assign ranks based on points (সমস্ত শিক্ষার্থীর জন্য র‍্যাঙ্ক নির্ধারণ)
    ranked_students = []
    for index, student in enumerate(students_with_points, start=1):
        ranked_students.append({
            'rank': index,
            'name': student['name'],
            'subject': student['subject'],
            'points': student['points']
        })

    # এখন নাম দিয়ে ফিল্টার করুন (র‍্যাঙ্ক নির্ধারণের পরে)
    if search_name:
        ranked_students = [student for student in ranked_students 
                          if search_name.lower() in student['name'].lower()]

    # সব unique subject এর list
    all_subjects = Exam.objects.values_list('subject', flat=True).distinct()

    return render(request, 'home/mcq/vec_mcq_rank.html', {
        'rankings': ranked_students,
        'subjects': all_subjects,
        'selected_subject': subject,
        'search_name': search_name
    })

# New result system views

