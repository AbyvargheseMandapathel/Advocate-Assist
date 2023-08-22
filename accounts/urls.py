# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer/pending_approval/', views.pending_approval_view, name='pending_approval'),
    path('lawyer/rejection_reason/<int:user_id>/', views.rejection_reason_view, name='rejection_reason'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]
