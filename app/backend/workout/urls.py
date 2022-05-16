from django.urls import path

from . import views

urlpatterns = [
    path('lastTestResult/<int:user_id>', views.LastTestResultView.as_view()),
    path('testResult/<int:user_id>', views.SaveTestResultView.as_view()),
    path('createRoutine/<int:user_id>', views.CreateRoutineView.as_view()),
    path('todayRoutine/<int:user_id>', views.TodayRoutineView.as_view()),
    path('userWorkoutInfo/<str:workout>/<int:user_id>', views.GetUserWorkoutInfo.as_view()),
    path('changeUserWorkoutInfo/<str:workout>/<str:date>/<int:user_id>', views.ChangeUserWorkoutInfo.as_view()),
    path('workoutResult/<str:workout>/<str:date>/<int:user_id>', views.WorkoutResultView.as_view()),
    path('startDateTime/<str:workout>/<str:date>/<int:user_id>', views.SaveStartDateTimeView.as_view()),
    path('endDateTime/<str:workout>/<str:date>/<int:user_id>', views.SaveEndDateTimetView.as_view()),
    path('changeWorkoutFeedback/<str:workout>/<int:user_id>', views.WorkoutFeedbackView.as_view()),
    path('extraWorkout/<int:user_id>', views.CreateExtraWorkoutView.as_view()),
]
