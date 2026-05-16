from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    path('adopt/<int:pet_id>/', views.adopt_pet_view, name='adopt_pet'),
    path('custom-admin/', views.admin_dashboard_view, name='custom_admin'),
]
