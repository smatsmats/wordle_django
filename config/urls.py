from django.urls import path

from solver import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/solve", views.api_solve, name="api_solve"),
    path("healthz", views.healthz, name="healthz"),
]
