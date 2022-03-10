from django.urls import path

from . import views

urlpatterns = [
    path('<str:date>/<int:user_id>', views.DietView.as_view()),
]
