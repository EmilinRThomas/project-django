from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    path('packages/', views.package_list, name='packages'),
    path('book/<int:pk>/', views.book_package, name='book_package'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/package/create/', views.create_package, name='create_package'),
    path('vendor/package/<int:pk>/edit/', views.edit_package, name='edit_package'),
    path('vendor/package/<int:pk>/delete/', views.delete_package, name='delete_package'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/packages/<int:pk>/approve/', views.approve_package, name='approve_package'),
    path('admin/packages/<int:pk>/reject/', views.reject_package, name='reject_package'),
]
