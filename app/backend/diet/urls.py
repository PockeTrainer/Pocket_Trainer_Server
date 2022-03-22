from django.urls import path

from . import views

urlpatterns = [
    path('createTargetKcal/<int:user_id>', views.CreateTargetKcalView.as_view()),
    path('<str:date>/<int:user_id>', views.DietView.as_view()),
]
