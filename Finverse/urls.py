"""
URL configuration for Finverse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse 

def home_view(request):
    html = """
    <html>
        <head>
            <title>Finverse API</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; background: #f4f4f9; }
                h1 { color: #333; }
                a { text-decoration: none; color: #007bff; font-weight: bold; }
                a:hover { color: #0056b3; }
            </style>
        </head>
        <body>
            <h1>💰 Welcome to Finverse API</h1>
            <p>The backend is running successfully.</p>
            <hr style="width:50%; margin: 20px auto;">
            <p>
                <a href="/admin/">🔐 Admin Panel</a> | 
                <a href="/api/docs/">📖 Documentation</a>
            </p>
        </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/loans/", include("loans.urls")),
]
