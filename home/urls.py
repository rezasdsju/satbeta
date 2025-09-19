# home/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('programming-hub/', views.programming_hub_view, name='program_hub'),
    path("python-child-1/", views.python_child_1_view, name="python_child_1"),
    path("python-runner/", views.python_runner, name="python_runner"),
    path('djn-minor-details/', views.django_minor_details_view, name='djn_minor_details'),
    path("user-auth-tutorial/", views.user_auth_tutorial_view, name="user_auth"),
    path('layout_1/',views.ban_ara_eng_layout,name='layout_1'),

    path('tutorials-hub/', views.tutorials_hub_view, name='tutorial_hub'),
    path('confusion-matrix/', views.conf_matrix_view, name='conf_matrix'),

    # PDF-related URLs - শুধু একটি pdf_hub রাখুন
    path('pdf-hub/', views.pdf_hub_view, name='pdf_hub'),
    path('vector-pdf/', views.vector_pdf_view, name='vec_pdf'),
    path('pdf/upload/', views.upload_pdf, name='upload_pdf'),

    path('result_for/', views.result_for_view, name='result_for'),
    # Result system URLs
    path('school_mark_input/', views.school_mark_input, name='school_mark_input'),
    path('show_school_result/', views.show_school_result, name='show_school_result'),
    path('download_single_csv/<int:result_id>/', views.download_single_csv, name='download_single_csv'),
    path('download_single_pdf/<int:result_id>/', views.download_single_pdf, name='download_single_pdf'),
    path('download_all_csv/', views.download_all_csv, name='download_all_csv'),
    path('download_all_pdf/', views.download_all_pdf, name='download_all_pdf'),
    path('clear_all_results/', views.clear_all_results, name='clear_all_results'),
    # University result system URLs
    path('varsity-mark-input/', views.varsity_mark_input, name='varsity_mark_input'),
    path('show-varsity-result/', views.show_varsity_result, name='show_varsity_result'),
    path('varsity-download-single-csv/<int:result_id>/', views.varsity_download_single_csv, name='varsity_download_single_csv'),
    path('varsity-download-single-pdf/<int:result_id>/', views.varsity_download_single_pdf, name='varsity_download_single_pdf'),
    path('varsity-download-all-csv/', views.varsity_download_all_csv, name='varsity_download_all_csv'),
    path('varsity-download-all-pdf/', views.varsity_download_all_pdf, name='varsity_download_all_pdf'),
    path('varsity-clear-all-results/', views.varsity_clear_all_results, name='varsity_clear_all_results'),


    path('mcq_hub/', views.mcq_hub_view, name='mcq_hub'),
    path('vector_main_mcq/', views.vector_mcq_view, name='vector_main_mcq'),
    path('narration/', views.narration_view, name='narration'),
    path('vocabulary/', views.vocabulary_view, name='vocab_main'),
    path('bcs_english/', views.bcs_english_view, name='bcs_english'),
    path("ranking/", views.ranking_view, name="vec_mcq_rank"),
    path("submit_exam_result/", views.submit_exam, name="submit_exam_result"),
]