"""
URL configuration for Studentinfo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from info import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.registration,name='register'),
    path('log/',views.lon,name='login'),
    path('suc/',views.success,name='success'),
    path('', views.shome, name='home'),
    path('marks/', views.marks_view, name='marks'),
    path('addmarks/', views.add_marks, name='amarks'),
    path('details/', views.sdetails, name='details'),
    path('search/', views.ssearch, name='search'),
    path('logout/', views.logout_view, name='logout'),
    path('student/',views.sstudent,name='student'),
    path('admin-login/', views.Adminlogin, name='alogin'),
    path('Admin/',views.admin1,name='admin'),
    path('adminportal/', views.admin_students, name='admin_students'),
    path('adminportal/update/<int:rollno>/', views.admin_update_delete, name='admin_update_delete'),
    path('adminportal/marks/', views.admin_marks_view, name='admin_marks'),



]
if settings.DEBUG:  # Only serve media in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
