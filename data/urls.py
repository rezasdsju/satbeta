from django.urls import path
from . import views

urlpatterns = [
    #path('upload/', views.upload_dataset, name='upload_dataset'),
    #path('analytics/bivariate/', views.bivariate_analysis, name='bivariate_analysis'),
    #path('analytics/bivariate/download/<str:format>/', views.download_bivariate, name='download_bivariate'),
    path('analytics_hub/', views.analytics_hub_view, name='analytics_hub'),
]