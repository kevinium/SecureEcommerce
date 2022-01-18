"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from ecom.settings import MEDIA_ROOT
from signup.views import signup,go_to_setup,accept_otp,login_req 
from django.conf.urls import url
from buyer.views import home_page,addSeller

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buyer/',include('buyer.urls',namespace='buyer')),
    url('signup/', signup, name = 'signup' ),
    url('accounts/login/', login_req, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    url('setup-otp/',go_to_setup , name = 'setup-otp' ),
    url('otp/',accept_otp, name = 'accept-otp' ),
    path('',home_page ),
    path('upgrade', addSeller),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)