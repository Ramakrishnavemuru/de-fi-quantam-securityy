from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('quantum-crypto/', include('quantum_crypto.urls')),
    path('ai-security/', include('ai_security.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

