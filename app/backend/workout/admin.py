
from django.contrib import admin

# Register your models here.
from .models import DayHistoryWorkoutWrongPoses, WorkoutInfo, DayHistoryWorkout

admin.site.register(WorkoutInfo)
admin.site.register(DayHistoryWorkout)
# admin.site.register(DayHistoryExtraWorkout)
admin.site.register(DayHistoryWorkoutWrongPoses)
# admin.site.register(DayHistoryExtraWorkoutWrongPoses)