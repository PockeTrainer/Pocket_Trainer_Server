
from django.contrib import admin

# Register your models here.
from .models import DayHistoryExtraWorkoutWrongPoses, DayHistoryWorkoutWrongPoses, WorkoutInfo, DayHistoryWorkout, DayHistoryExtraWorkout

admin.site.register(WorkoutInfo)
admin.site.register(DayHistoryWorkout)
admin.site.register(DayHistoryExtraWorkout)
admin.site.register(DayHistoryWorkoutWrongPoses)
admin.site.register(DayHistoryExtraWorkoutWrongPoses)