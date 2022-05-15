from django.urls import path

from . import views

urlpatterns = [
    path('mainpageInfo/<int:user_id>', views.MainPageInfoView.as_view()),
    path('month/<str:year_month>/<int:user_id>', views.MonthHistoryView.as_view()),
    path('day/<str:date>/<int:user_id>', views.DayHistoryView.as_view()),
    path('day/<str:date>/<str:workout>/<int:user_id>', views.DayHistoryWorkoutInfoView.as_view()),
    path('workoutGraph/<str:workout>/<int:user_id>', views.WorkoutGraphView.as_view()),
]

