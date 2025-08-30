from django.urls import path
from . import views, api_views

urlpatterns = [
    #web endpoints
    path('', views.home, name='home'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issue/create/', views.issue_create, name='issue_create'),
    path('issue/<int:pk>/edit/', views.issue_edit, name='issue_edit'),
    path('issue/<int:pk>/delete/', views.issue_delete, name='issue_delete'),
    path('issue/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),


    # API endpoints
    path('api/issues/', api_views.IssueListCreateAPI.as_view(), name='api_issues'),
    path('api/issues/<int:pk>/', api_views.IssueDetailAPI.as_view(), name='api_issue_detail'),
    path('api/comments/', api_views.CommentListCreateAPI.as_view(), name='api_comments'),
]
