"""referral_mate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from referral_app import views
from referral_app.views import CodeCreate, FriendDetail, CodeDetail



urlpatterns = [
    path('', views.home, name='codes-list'),
    path('admin/', admin.site.urls),
    path('referral_app/', include('referral_app.urls')),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='referral_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='referral_app/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('codes/new', CodeCreate.as_view(), name='code-create'),
    path('code/<int:pk>', CodeDetail.as_view(), name='code-detail'),
    path('friends/<int:pk>', FriendDetail.as_view(
        template_name='referral_app/friend_detail.html'),
        name='friend-detail'),
    path('brand/<int:pk>', views.brand_detail, name='brand-detail')
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
