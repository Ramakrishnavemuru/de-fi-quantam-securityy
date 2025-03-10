from django.urls import path
from . import views

urlpatterns = [
    path('keys/', views.quantum_key_list_view, name='quantum_key_list'),
    path('keys/generate/', views.generate_quantum_key_view, name='generate_quantum_key'),
    path('keys/<str:key_id>/rotate/', views.rotate_quantum_key_view, name='rotate_quantum_key'),
]

