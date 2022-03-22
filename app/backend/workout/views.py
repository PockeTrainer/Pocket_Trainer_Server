
from asyncio.windows_events import NULL
from typing import AsyncGenerator
from django.shortcuts import render
#generics

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User, UserTestResult, UserWorkoutInfo, UserWorkoutRoutine
from .models import DayHistoryWorkout, WorkoutInfo
from .serializers import DayHistorySerializer

from rest_framework.permissions import AllowAny, IsAuthenticated

from datetime import datetime

class CreateRoutineView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        date = datetime.now().date()
        DayHistory_Workout = DayHistoryWorkout.objects.filter(user_id = user, create_date=date)
        
        try:
            #해당일 계획 존재 하지 않을 때 운동루틴 레벨에 맞게 계획 세우기
            if len(DayHistory_Workout) == 0 :
                try:
                    User_WorkoutRoutine = UserWorkoutRoutine.objects.get(user_id = user)
                except UserWorkoutRoutine.DoesNotExist:
                    return Response({"error":"오늘의 운동 루틴 생성 실패, 체력평가 결과 필요"}, status=400)
                todayRoutine = User_WorkoutRoutine.workout_routine
                
                # row 추가 code
                if (todayRoutine == 0) :
                    # 가슴 운동
                    Workout_Info = WorkoutInfo.objects.get(workout_name="bench_press")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    Workout_Info = WorkoutInfo.objects.get(workout_name="incline_press")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    Workout_Info = WorkoutInfo.objects.get(workout_name="pec_dec_fly")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    #삼두 운동
                    triceps_seq = User_WorkoutRoutine.triceps_seq  #삼두 순서
                    if triceps_seq == 0:
                        workout = "cable_push_down"
                    elif triceps_seq == 1:
                        workout = "lying_triceps_extension"
                    elif triceps_seq == 2:
                        workout = "dumbbell_kickback"

                    Workout_Info = WorkoutInfo.objects.get(workout_name=workout)
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    #복부 운동
                    Workout_Info = WorkoutInfo.objects.get(workout_name="crunch")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_cnt = User_WorkoutInfo.target_cnt
                    created_DayHistory_Workout.save()

                elif (todayRoutine == 1) :
                    # 등 운동
                    Workout_Info = WorkoutInfo.objects.get(workout_name="lat_pull_down")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    Workout_Info = WorkoutInfo.objects.get(workout_name="seated_row")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    Workout_Info = WorkoutInfo.objects.get(workout_name="one_arm_dumbbell_row")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    # 이두 운동
                    biceps_seq = User_WorkoutRoutine.biceps_seq  #이두 순서
                    if biceps_seq == 0:
                        workout = "easy_bar_curl"
                    elif biceps_seq == 1:
                        workout = "arm_curl"
                    elif biceps_seq == 2:
                        workout = "hammer_curl"

                    Workout_Info = WorkoutInfo.objects.get(workout_name=workout)
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    # 복부 운동
                    Workout_Info = WorkoutInfo.objects.get(workout_name="seated_knees_up")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_cnt = User_WorkoutInfo.target_cnt
                    created_DayHistory_Workout.save()

                else:
                    # 어깨 운동
                    Workout_Info = WorkoutInfo.objects.get(workout_name="dumbbell_shoulder_press")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()


                    Workout_Info = WorkoutInfo.objects.get(workout_name="side_lateral_raise")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()


                    Workout_Info = WorkoutInfo.objects.get(workout_name="reverse_peck_deck_fly")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    # 하체 운동
                    Workout_Info = WorkoutInfo.objects.get(workout_name="squat")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()


                    Workout_Info = WorkoutInfo.objects.get(workout_name="leg_press")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()


                    Workout_Info = WorkoutInfo.objects.get(workout_name="leg_extension")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_kg = User_WorkoutInfo.target_kg
                    created_DayHistory_Workout.save()

                    # 복부 운동
                    Workout_Info = WorkoutInfo.objects.get(workout_name="plank")
                    User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id = user, workout_name = Workout_Info)

                    created_DayHistory_Workout = DayHistoryWorkout.objects.create(user_id=user, create_date=date, workout_name=Workout_Info)
                    created_DayHistory_Workout.target_time = User_WorkoutInfo.target_time
                    created_DayHistory_Workout.save()
                
                return Response({
                        "code" : "200",
                        "message" : "workout row 생성 완료",
                    })
            else:
                return Response({"error":"오늘의 운동 계획이 이미 생성되었습니다"}, status=400)
        except:
            return Response({"error":"workout row 생성 실패."}, status=400)

#제일 최근 평가 기록 가져오기
class LastTestResultView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):

        user = User.objects.get(id=user_id)

        try:
            UserTest_Result = UserTestResult.objects.filter(user_id=user).last()

            upperbody_strength = UserTest_Result.upperbody_strength
            stomach_strength = UserTest_Result.stomach_strength
            lowerbody_strength = UserTest_Result.lowerbody_strength
            pushup_cnt = UserTest_Result.pushup_cnt
            situp_cnt = UserTest_Result.situp_cnt
            squat_cnt = UserTest_Result.squat_cnt
            date = UserTest_Result.create_date

            return Response({
                    "code" : "200",
                    "message" : "최근 평가 기록 확인 완료",
                    "upperbody_strength" : upperbody_strength,
                    "stomach_strength" : stomach_strength,
                    "lowerbody_strength" : lowerbody_strength,
                    "pushup_cnt" : pushup_cnt,
                    "situp_cnt" : situp_cnt,
                    "squat_cnt" : squat_cnt,
                    "date" : date
                })
        except:
            return Response({"error":"최근 평가 기록이 존재하지 않습니다."}, status=400)


#체력측정 기록 저장
class SaveTestResultView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        today = datetime.now().date()
        age = today.year - user.birth.year
        if today.month < user.birth.month or (today.month == user.birth.month and today.day < user.birth.day) : 
            age -= 1
        
        #try:
        User_TestResult = UserTestResult.objects.create(user_id = user)
        
        User_TestResult.pushup_cnt = request.data['pushUp']
        User_TestResult.situp_cnt = request.data['sitUp']
        User_TestResult.squat_cnt = request.data['squat']
        
        # 남자 pushUp 등급
        if ("man" in user.gender) :
            if (age <= 19) :
                if (int(request.data.get('pushUp')) >= 30) :
                    User_TestResult.upperbody_strength = 1
                elif (22 <= int(request.data.get('pushUp')) < 30) :
                    User_TestResult.upperbody_strength = 2
                elif (14 <= int(request.data.get('pushUp')) < 22) :
                    User_TestResult.upperbody_strength = 3
                elif (6 <= int(request.data.get('pushUp')) < 14) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5
                
            elif (20 <= age <= 35) :
                if (int(request.data.get('pushUp')) >= 32) :
                    User_TestResult.upperbody_strength = 1
                elif (24 <= int(request.data.get('pushUp')) < 32) :
                    User_TestResult.upperbody_strength = 2
                elif (16 <= int(request.data.get('pushUp')) < 24) :
                    User_TestResult.upperbody_strength = 3
                elif (8 <= int(request.data.get('pushUp')) < 16) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5

            elif (36 <= age <= 49) :
                if (int(request.data.get('pushUp')) >= 30) :
                    User_TestResult.upperbody_strength = 1
                elif (22 <= int(request.data.get('pushUp')) < 30) :
                    User_TestResult.upperbody_strength = 2
                elif (14 <= int(request.data.get('pushUp')) < 22) :
                    User_TestResult.upperbody_strength = 3
                elif (6 <= int(request.data.get('pushUp')) < 14) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5
            
            elif (50 <= age <= 65) :
                if (int(request.data.get('pushUp')) >= 28) :
                    User_TestResult.upperbody_strength = 1
                elif (20 <= int(request.data.get('pushUp')) < 28) :
                    User_TestResult.upperbody_strength = 2
                elif (12 <= int(request.data.get('pushUp')) < 20) :
                    User_TestResult.upperbody_strength = 3
                elif (4 <= int(request.data.get('pushUp')) < 12) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5

            elif (66 <= age ) :
                if (int(request.data.get('pushUp')) >= 26) :
                    User_TestResult.upperbody_strength = 1
                elif (18 <= int(request.data.get('pushUp')) < 26) :
                    User_TestResult.upperbody_strength = 2
                elif (10 <= int(request.data.get('pushUp')) < 18) :
                    User_TestResult.upperbody_strength = 3
                elif (4 <= int(request.data.get('pushUp')) < 10) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5
        # 여자 pushUp 등급
        elif ("woman" in user.gender) :
            if (age <= 19) :
                if (int(request.data.get('pushUp')) >= 16) :
                    User_TestResult.upperbody_strength = 1
                elif (12 <= int(request.data.get('pushUp')) < 16) :
                    User_TestResult.upperbody_strength = 2
                elif (8 <= int(request.data.get('pushUp')) < 12) :
                    User_TestResult.upperbody_strength = 3
                elif (4 <= int(request.data.get('pushUp')) < 8) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5
                
            elif (20 <= age <= 35) :
                if (int(request.data.get('pushUp')) >= 20) :
                    User_TestResult.upperbody_strength = 1
                elif (16 <= int(request.data.get('pushUp')) < 20) :
                    User_TestResult.upperbody_strength = 2
                elif (12 <= int(request.data.get('pushUp')) < 16) :
                    User_TestResult.upperbody_strength = 3
                elif (8 <= int(request.data.get('pushUp')) < 12) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5

            elif (36 <= age <= 49) :
                if (int(request.data.get('pushUp')) >= 18) :
                    User_TestResult.upperbody_strength = 1
                elif (14 <= int(request.data.get('pushUp')) < 18) :
                    User_TestResult.upperbody_strength = 2
                elif (10 <= int(request.data.get('pushUp')) < 14) :
                    User_TestResult.upperbody_strength = 3
                elif (4 <= int(request.data.get('pushUp')) < 10) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5
            
            elif (50 <= age <= 65) :
                if (int(request.data.get('pushUp')) >= 18) :
                    User_TestResult.upperbody_strength = 1
                elif (14 <= int(request.data.get('pushUp')) < 18) :
                    User_TestResult.upperbody_strength = 2
                elif (10 <= int(request.data.get('pushUp')) < 14) :
                    User_TestResult.upperbody_strength = 3
                elif (4 <= int(request.data.get('pushUp')) < 10) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5

            elif (66 <= age ) :
                if (int(request.data.get('pushUp')) >= 16) :
                    User_TestResult.upperbody_strength = 1
                elif (12 <= int(request.data.get('pushUp')) < 16) :
                    User_TestResult.upperbody_strength = 2
                elif (8 <= int(request.data.get('pushUp')) < 12) :
                    User_TestResult.upperbody_strength = 3
                elif (4 <= int(request.data.get('pushUp')) < 8) :
                    User_TestResult.upperbody_strength = 4
                else :
                    User_TestResult.upperbody_strength = 5

        
        # 남자 윗몸 등급
        if ("man" in user.gender) :
            if (19 >= age) :
                if (int(request.data.get('sitUp')) >= 35) :
                    User_TestResult.stomach_strength = 1
                elif (27 <= int(request.data.get('sitUp')) < 35) :
                    User_TestResult.stomach_strength = 2
                elif (19 <= int(request.data.get('sitUp')) < 27) :
                    User_TestResult.stomach_strength = 3
                elif (11 <= int(request.data.get('sitUp')) < 19) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5

            if (20 <= age <= 35) :
                if (int(request.data.get('sitUp')) >= 37) :
                    User_TestResult.stomach_strength = 1
                elif (29 <= int(request.data.get('sitUp')) < 37) :
                    User_TestResult.stomach_strength = 2
                elif (21 <= int(request.data.get('sitUp')) < 29) :
                    User_TestResult.stomach_strength = 3
                elif (13 <= int(request.data.get('sitUp')) < 21) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5
                    
            if (36 <= age <= 49) :
                if (int(request.data.get('sitUp')) >= 35) :
                    User_TestResult.stomach_strength = 1
                elif (27 <= int(request.data.get('sitUp')) < 35) :
                    User_TestResult.stomach_strength = 2
                elif (19 <= int(request.data.get('sitUp')) < 27) :
                    User_TestResult.stomach_strength = 3
                elif (11 <= int(request.data.get('sitUp')) < 19) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5

                    
            if (50 <= age <= 65) :
                if (int(request.data.get('sitUp')) >= 33) :
                    User_TestResult.stomach_strength = 1
                elif (25 <= int(request.data.get('sitUp')) < 33) :
                    User_TestResult.stomach_strength = 2
                elif (17 <= int(request.data.get('sitUp')) < 25) :
                    User_TestResult.stomach_strength = 3
                elif (9 <= int(request.data.get('sitUp')) < 17) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5
            
            if (66 <= age) :
                if (int(request.data.get('sitUp')) >= 31) :
                    User_TestResult.stomach_strength = 1
                elif (23 <= int(request.data.get('sitUp')) < 31) :
                    User_TestResult.stomach_strength = 2
                elif (15 <= int(request.data.get('sitUp')) < 23) :
                    User_TestResult.stomach_strength = 3
                elif (7 <= int(request.data.get('sitUp')) < 15) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5
        # 여자 윗몸 등급
        elif ("woman" in user.gender) :
            if (19 >= age) :
                if (int(request.data.get('sitUp')) >= 31) :
                    User_TestResult.stomach_strength = 1
                elif (23 <= int(request.data.get('sitUp')) < 31) :
                    User_TestResult.stomach_strength = 2
                elif (15 <= int(request.data.get('sitUp')) < 23) :
                    User_TestResult.stomach_strength = 3
                elif (7 <= int(request.data.get('sitUp')) < 15) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5

            if (20 <= age <= 35) :
                if (int(request.data.get('sitUp')) >= 29) :
                    User_TestResult.stomach_strength = 1
                elif (21 <= int(request.data.get('sitUp')) < 29) :
                    User_TestResult.stomach_strength = 2
                elif (13 <= int(request.data.get('sitUp')) < 21) :
                    User_TestResult.stomach_strength = 3
                elif (5 <= int(request.data.get('sitUp')) < 13) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5
                    
            if (36 <= age <= 49) :
                if (int(request.data.get('sitUp')) >= 29) :
                    User_TestResult.stomach_strength = 1
                elif (21 <= int(request.data.get('sitUp')) < 29) :
                    User_TestResult.stomach_strength = 2
                elif (13 <= int(request.data.get('sitUp')) < 21) :
                    User_TestResult.stomach_strength = 3
                elif (5 <= int(request.data.get('sitUp')) < 13) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5

                    
            if (50 <= age <= 65) :
                if (int(request.data.get('sitUp')) >= 27) :
                    User_TestResult.stomach_strength = 1
                elif (19 <= int(request.data.get('sitUp')) < 27) :
                    User_TestResult.stomach_strength = 2
                elif (11 <= int(request.data.get('sitUp')) < 19) :
                    User_TestResult.stomach_strength = 3
                elif (4 <= int(request.data.get('sitUp')) < 11) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5
            
            if (66 <= age) :
                if (int(request.data.get('sitUp')) >= 27) :
                    User_TestResult.stomach_strength = 1
                elif (19 <= int(request.data.get('sitUp')) < 27) :
                    User_TestResult.stomach_strength = 2
                elif (11 <= int(request.data.get('sitUp')) < 19) :
                    User_TestResult.stomach_strength = 3
                elif (4 <= int(request.data.get('sitUp')) < 11) :
                    User_TestResult.stomach_strength = 4
                else :
                    User_TestResult.stomach_strength = 5

        # 남자 스쿼트 등급
        if ("man" in user.gender) :
            if (19 >= age) :
                if (int(request.data.get('squat')) >= 40) :
                    User_TestResult.lowerbody_strength = 1
                elif (30 <= int(request.data.get('squat')) < 40) :
                    User_TestResult.lowerbody_strength = 2
                elif (20 <= int(request.data.get('squat')) < 30) :
                    User_TestResult.lowerbody_strength = 3
                elif (10 <= int(request.data.get('squat')) < 20) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5

            if (20 <= age <= 35) :
                if (int(request.data.get('squat')) >= 45) :
                    User_TestResult.lowerbody_strength = 1
                elif (35 <= int(request.data.get('squat')) < 45) :
                    User_TestResult.lowerbody_strength = 2
                elif (25 <= int(request.data.get('squat')) < 35) :
                    User_TestResult.lowerbody_strength = 3
                elif (15 <= int(request.data.get('squat')) < 25) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5

            if (36 <= age <= 49) :
                if (int(request.data.get('squat')) >= 45) :
                    User_TestResult.lowerbody_strength = 1
                elif (35 <= int(request.data.get('squat')) < 45) :
                    User_TestResult.lowerbody_strength = 2
                elif (25 <= int(request.data.get('squat')) < 35) :
                    User_TestResult.lowerbody_strength = 3
                elif (15 <= int(request.data.get('squat')) < 25) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5

            if (50 <= age <= 65) :
                if (int(request.data.get('squat')) >= 40) :
                    User_TestResult.lowerbody_strength = 1
                elif (30 <= int(request.data.get('squat')) < 40) :
                    User_TestResult.lowerbody_strength = 2
                elif (20 <= int(request.data.get('squat')) < 30) :
                    User_TestResult.lowerbody_strength = 3
                elif (10 <= int(request.data.get('squat')) < 20) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5
            
            if (66 <= age) :
                if (int(request.data.get('squat')) >= 35) :
                    User_TestResult.lowerbody_strength = 1
                elif (25 <= int(request.data.get('squat')) < 35) :
                    User_TestResult.lowerbody_strength = 2
                elif (15 <= int(request.data.get('squat')) < 25) :
                    User_TestResult.lowerbody_strength = 3
                elif (6 <= int(request.data.get('squat')) < 15) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5

        # 여자 스쿼트 등급
        if ("woman" in user.gender) :
            if (19 >= age) :
                if (int(request.data.get('squat')) >= 40) :
                    User_TestResult.lowerbody_strength = 1
                elif (30 <= int(request.data.get('squat')) < 40) :
                    User_TestResult.lowerbody_strength = 2
                elif (20 <= int(request.data.get('squat')) < 30) :
                    User_TestResult.lowerbody_strength = 3
                elif (10 <= int(request.data.get('squat')) < 20) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5

            if (20 <= age <= 35) :
                if (int(request.data.get('squat')) >= 40) :
                    User_TestResult.lowerbody_strength = 1
                elif (30 <= int(request.data.get('squat')) < 40) :
                    User_TestResult.lowerbody_strength = 2
                elif (20 <= int(request.data.get('squat')) < 30) :
                    User_TestResult.lowerbody_strength = 3
                elif (10 <= int(request.data.get('squat')) < 20) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5

            if (36 <= age <= 49) :
                if (int(request.data.get('squat')) >= 40) :
                    User_TestResult.lowerbody_strength = 1
                elif (30 <= int(request.data.get('squat')) < 40) :
                    User_TestResult.lowerbody_strength = 2
                elif (20 <= int(request.data.get('squat')) < 30) :
                    User_TestResult.lowerbody_strength = 3
                elif (10 <= int(request.data.get('squat')) < 20) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5

            if (50 <= age <= 65) :
                if (int(request.data.get('squat')) >= 35) :
                    User_TestResult.lowerbody_strength = 1
                elif (25 <= int(request.data.get('squat')) < 35) :
                    User_TestResult.lowerbody_strength = 2
                elif (15 <= int(request.data.get('squat')) < 25) :
                    User_TestResult.lowerbody_strength = 3
                elif (6 <= int(request.data.get('squat')) < 15) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5
            
            if (66 <= age) :
                if (int(request.data.get('squat')) >= 35) :
                    User_TestResult.lowerbody_strength = 1
                elif (25 <= int(request.data.get('squat')) < 35) :
                    User_TestResult.lowerbody_strength = 2
                elif (15 <= int(request.data.get('squat')) < 25) :
                    User_TestResult.lowerbody_strength = 3
                elif (6 <= int(request.data.get('squat')) < 15) :
                    User_TestResult.lowerbody_strength = 4
                else :
                    User_TestResult.lowerbody_strength = 5
        
        User_TestResult.save()

        #UserWorkoutInfo 테이블 update or create (운동 루틴, 각 운동별 무게 추천)
        #등급으로 각 운동별 추천 무게 설정
        kg = 0
        cnt = 0
        time = "00:01:00"

        # 가슴 (chest)
        Workout_Info = WorkoutInfo.objects.get(workout_name="bench_press")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()
        
        Workout_Info = WorkoutInfo.objects.get(workout_name="incline_press")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="pec_dec_fly")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        # 등 (back)
        Workout_Info = WorkoutInfo.objects.get(workout_name="lat_pull_down")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="seated_row")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="one_arm_dumbbell_row")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        # 어깨
        Workout_Info = WorkoutInfo.objects.get(workout_name="dumbbell_shoulder_press")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="side_lateral_raise")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="reverse_peck_deck_fly")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        # 삼두
        Workout_Info = WorkoutInfo.objects.get(workout_name="cable_push_down")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="lying_triceps_extension")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="dumbbell_kickback")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        # 이두
        Workout_Info = WorkoutInfo.objects.get(workout_name="easy_bar_curl")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="arm_curl")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()
        
        Workout_Info = WorkoutInfo.objects.get(workout_name="hammer_curl")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save() 

        # 복부 (stomach)
        Workout_Info = WorkoutInfo.objects.get(workout_name="crunch")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_cnt = 15
        User_WorkoutInfo.save()          

        Workout_Info = WorkoutInfo.objects.get(workout_name="seated_knees_up")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_cnt = 10
        User_WorkoutInfo.save() 

        Workout_Info = WorkoutInfo.objects.get(workout_name="plank")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_time = time 
        User_WorkoutInfo.save() 

        # 하체
        Workout_Info = WorkoutInfo.objects.get(workout_name="squat")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()

        Workout_Info = WorkoutInfo.objects.get(workout_name="leg_press")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save()
        
        Workout_Info = WorkoutInfo.objects.get(workout_name="leg_extension")
        User_WorkoutInfo, created = UserWorkoutInfo.objects.update_or_create(user_id = user, workout_name = Workout_Info)
        User_WorkoutInfo.target_kg = kg
        User_WorkoutInfo.save() 
        
        if created:
            UserWorkoutRoutine.objects.create(
                user_id= user, 
                workout_routine = 0,
                triceps_seq = 0,
                biceps_seq = 0
            )

        return Response({
                "code" : 200,
                "message" : "체력평가 기록 저장 완료"
            })
        #except:
        #    return Response({"error":"체력평가 기록 저장 실패."}, status=400)

#오늘의 루틴 정보 호출
class TodayRoutineView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
 #       try:
        user = User.objects.get(id=user_id)

        #오늘의 루틴 기록
        today = datetime.now().date()
        DayHistory_Workout_q = DayHistoryWorkout.objects.filter(user_id=user, create_date=today)
        DayHistoryWorkout_Serializer = DayHistorySerializer(DayHistory_Workout_q, many=True)    

        try:
            User_WorkoutRoutine = UserWorkoutRoutine.objects.get(user_id = user)
            
            # routine : 오늘 루틴 순서
            # 오늘 운동 수행 x -> 오늘 루틴
            if (User_WorkoutRoutine.last_routine0_date != today 
                    and User_WorkoutRoutine.last_routine1_date != today
                    and User_WorkoutRoutine.last_routine2_date != today):
                routine = User_WorkoutRoutine.workout_routine
            # 오늘 운동 수행 o -> -1 루틴
            else:
                routine = (User_WorkoutRoutine.workout_routine+2) % 3

            # 루틴 생성 완료 상태
            if routine == 0:
                last_routine_date = User_WorkoutRoutine.last_routine0_date
            elif routine == 1:
                last_routine_date = User_WorkoutRoutine.last_routine1_date
            elif routine == 2:
                last_routine_date = User_WorkoutRoutine.last_routine2_date

        # 아직 체력 평가 X 상태
        except UserWorkoutRoutine.DoesNotExist:
            last_routine_date = None

        return Response({
                    "code" : 200,
                    "message" : "오늘의 루틴 페이지 정보 호출 완료",
                    "todayRoutine" : DayHistoryWorkout_Serializer.data,
                    "last_routine_date" : last_routine_date
                })
#3        except:
 #           return Response({"error":"오늘의 루틴 페이지 정보 호출 실패."}, status=400)

#운동측정 전 무게 or 갯수 or 시간 호출 
class GetUserWorkoutInfo(APIView):
    permission_classes = [AllowAny]
    def get(self, request, workout, user_id):
        is_first = False    #해당 운동 처음 하는지(무게 추천)
        try:
            user = User.objects.get(id=user_id)
            Workout_Info = WorkoutInfo.objects.get(workout_name=workout)

            User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id=user, workout_name=Workout_Info)

            #이전에 해당 운동 무게 측정x 상태
            if(User_WorkoutInfo.last_update_date == None) :
                is_first = True

            User_WorkoutInfo.save()

            return Response({
                        "code" : 200,
                        "message" : "유저 운동정보 호출 완료",
                        "is_first" : is_first,
                        "target_kg" : User_WorkoutInfo.target_kg,
                        "target_cnt" : User_WorkoutInfo.target_cnt,
                        "target_time" : User_WorkoutInfo.target_time,
                        "last_update_date" : User_WorkoutInfo.last_update_date,
                        "workout_feedback" : User_WorkoutInfo.workout_feedback,
                    })
        except:
            return Response({"error" : "유저 운동정보 호출 실패"}, status=400)


#운동측정 전 무게 or 갯수 or 시간 조절 
class ChangeUserWorkoutInfo(APIView):
    permission_classes = [AllowAny]
    def put(self, request, workout, date, user_id):
        #try:
        user = User.objects.get(id=user_id)
        Workout_Info = WorkoutInfo.objects.get(workout_name=workout)
        User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id=user, workout_name=Workout_Info)

        DayHistory_Workout = DayHistoryWorkout.objects.get(user_id=user, workout_name=Workout_Info, create_date=date)

        if('target_kg' in request.data) :
            User_WorkoutInfo.target_kg = request.data['target_kg']
            DayHistory_Workout.target_kg = request.data['target_kg']
        elif('target_cnt' in request.data) :
            User_WorkoutInfo.target_cnt = request.data['target_cnt']
            DayHistory_Workout.target_cnt = request.data['target_cnt']
        elif('target_time' in request.data) :
            User_WorkoutInfo.target_time = request.data['target_time']
            DayHistory_Workout.target_time = request.data['target_time']

        User_WorkoutInfo.workout_feedback = 0
        User_WorkoutInfo.last_update_date = date

        User_WorkoutInfo.save()
        DayHistory_Workout.save()

        return Response({
                    "code" : 200,
                    "message" : "유저 운동정보, 해당일 target 수정 완료",
                })
        #except:
        #    return Response({"error" : "유저 운동정보 변경 실패"}, status=400)

#운동 시작 시간 저장
class SaveStartDateTimeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, workout, date, user_id):
        try:
            user = User.objects.get(id=user_id)
            Workout_Info = WorkoutInfo.objects.get(workout_name=workout)     

            #오늘의 루틴 기록
            DayHistory_Workout_q = DayHistoryWorkout.objects.get(user_id=user, create_date=date, workout_name=Workout_Info)

            today = datetime.now()
            DayHistory_Workout_q.start_datetime = today
            DayHistory_Workout_q.save()

            return Response({
                    "code" : 200,
                    "message" : "운동 시작 시간 저장 완료",
                })
        except:
            return Response({"error" : "운동 시작 시간 저장 실패"}, status=400)

#운동 종료 시간 저장
class SaveEndDateTimetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, workout, date, user_id):
        try:
            user = User.objects.get(id=user_id)
            Workout_Info = WorkoutInfo.objects.get(workout_name=workout)     

            #오늘의 루틴 기록
            DayHistory_Workout_q = DayHistoryWorkout.objects.get(user_id=user, create_date=date, workout_name=Workout_Info)

            today = datetime.now()
            DayHistory_Workout_q.end_datetime = today
            DayHistory_Workout_q.save()

            return Response({
                    "code" : 200,
                    "message" : "운동 종료 시간 저장 완료",
                })  
        except:
            return Response({"error" : "운동 종료 시간 저장 실패"}, status=400)
            
#운동측정 기록 update
class WorkoutResultView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, workout, date, user_id):
        # try:
        user = User.objects.get(id=user_id)
        Workout_Info = WorkoutInfo.objects.get(workout_name=workout)

        DayHistory_Workout = DayHistoryWorkout.objects.get(user_id=user, create_date=date, workout_name=Workout_Info)
        DayHistory_Workout.workout_set = request.data['workout_set']
        DayHistory_Workout.workout_time = request.data['workout_time']

        User_WorkoutRoutine = UserWorkoutRoutine.objects.get(user_id = user)    

        # 아직 완료하지 않은 운동이고 해당 운동이 마지막 세트면 
        if (not DayHistory_Workout.is_clear and int(request.data['workout_set']) == 5) :
            #해당 운동 is_clear => True 
            DayHistory_Workout.is_clear = True
            DayHistory_Workout.save()

            #삼두 운동이면 삼두 순서+1
            if (workout in ['cable_push_down', 'lying_triceps_extension', 'dumbbell_kickback']):
                User_WorkoutRoutine.triceps_seq = (User_WorkoutRoutine.triceps_seq+1) % 3
            #이두 운동이면 이두 순서+1    
            elif (workout in ['easy_bar_curl', 'arm_curl', 'hammer_curl']):
                User_WorkoutRoutine.biceps_seq = (User_WorkoutRoutine.biceps_seq+1) % 3

            today_workout = DayHistoryWorkout.objects.filter(user_id=user, create_date=date)
            cleared_workout = DayHistoryWorkout.objects.filter(user_id=user, create_date=date, is_clear=True)
            percentage = len(cleared_workout) / len(today_workout)

            # 아직 오늘 루틴 갱신X  &  오늘 clear 운동 50% 이상 -> 최근 루틴 완료 날짜 갱신, 루틴 + 1
            if (User_WorkoutRoutine.workout_routine == 0):
                if (User_WorkoutRoutine.last_routine0_date != date 
                    and User_WorkoutRoutine.last_routine1_date != date
                    and User_WorkoutRoutine.last_routine2_date != date
                    and percentage >= 0.5):
                    User_WorkoutRoutine.last_routine0_date = date
                    User_WorkoutRoutine.workout_routine = (User_WorkoutRoutine.workout_routine+1)%3
            elif (User_WorkoutRoutine.workout_routine == 1):
                if (User_WorkoutRoutine.last_routine0_date != date 
                    and User_WorkoutRoutine.last_routine1_date != date
                    and User_WorkoutRoutine.last_routine2_date != date
                    and percentage >= 0.5):
                    User_WorkoutRoutine.last_routine1_date = date
                    User_WorkoutRoutine.workout_routine = (User_WorkoutRoutine.workout_routine+1)%3
            elif (User_WorkoutRoutine.workout_routine == 2):
                if (User_WorkoutRoutine.last_routine0_date != date 
                    and User_WorkoutRoutine.last_routine1_date != date
                    and User_WorkoutRoutine.last_routine2_date != date
                    and percentage >= 0.5):
                    User_WorkoutRoutine.last_routine2_date = date
                    User_WorkoutRoutine.workout_routine = (User_WorkoutRoutine.workout_routine+1)%3

        #DayHistory_Workout.save()
        User_WorkoutRoutine.save()

        return Response({
                    "code" : 200,
                    "message" : "운동 기록 저장 완료",
            })
        # except:
        #     return Response({"error" : "운동 기록 저장 실패"}, status=400)

#운동측정 후 피드백 반영
class WorkoutFeedbackView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, workout, user_id):
        try:
            user = User.objects.get(id=user_id)
            Workout_Info = WorkoutInfo.objects.get(workout_name=workout)

            User_WorkoutInfo = UserWorkoutInfo.objects.get(user_id=user, workout_name=Workout_Info)
            User_WorkoutInfo.workout_feedback = request.data['feedback']

            #feedback에 따른 무게 수정
            #덤벨
            if (workout in ['one_arm_dumbbell_row', 'dumbbell_shoulder_press', 'side_lateral_raise', 'lying_triceps_extension', 'dumbbell_kickback', 'hammer_curl']):
                # 가벼움
                if (int(request.data['feedback']) == 1):
                    User_WorkoutInfo.target_kg += 1
                # 무거움
                elif (int(request.data['feedback']) == 2):
                    if (User_WorkoutInfo.target_kg - 1) > 0:
                        User_WorkoutInfo.target_kg -= 1       
                    else:
                        Response({"error" : "feedback 반영 실패, 현재 최소"}, status=400)
            #원형 추 사용
            elif (workout in ['bench_press', 'incline_press', 'easy_bar_curl', 'squat', 'leg_press']):
                # 가벼움
                if (int(request.data['feedback']) == 1):
                    User_WorkoutInfo.target_kg += 5
                # 무거움
                elif (int(request.data['feedback']) == 2):
                    if (User_WorkoutInfo.target_kg - 5) > 0:
                        User_WorkoutInfo.target_kg -= 5       
                    else:
                        Response({"error" : "feedback 반영 실패, 현재 최소"}, status=400)     
            #머신 사용 (단위: 파운드)
            elif (workout in ['pec_dec_fly', 'lat_pull_dow', 'seated_row', 'reverse_peck_deck_fly', 'cable_push_down', 'arm_curl', 'leg_extension']):
                # 가벼움
                if (int(request.data['feedback']) == 1):
                    User_WorkoutInfo.target_kg += 5
                # 무거움
                elif (int(request.data['feedback']) == 2):
                    if (User_WorkoutInfo.target_kg - 1) > 0:
                        User_WorkoutInfo.target_kg -= 1       
                    else:
                        Response({"error" : "feedback 반영 실패, 현재 최소"}, status=400)          
            #횟수 조정
            elif (workout in ['crunch', 'seated_knees_up']):
                # 쉬움
                if (int(request.data['feedback']) == 1):
                    User_WorkoutInfo.target_cnt += 2
                # 어려움
                elif (int(request.data['feedback']) == 2):
                    if (User_WorkoutInfo.target_cnt - 2) > 0:
                        User_WorkoutInfo.target_cnt -= 2       
                    else:
                        Response({"error" : "feedback 반영 실패, 현재 최소"}, status=400)  
            #시간 조정
            elif (workout in ['plank']):
                # 쉬움
                if (int(request.data['feedback']) == 1):
                    User_WorkoutInfo.target_time += "00:00:10" 
                # 어려움
                elif (int(request.data['feedback']) == 2):
                    if (User_WorkoutInfo.target_time - "00:00:10" ) > 0:
                        User_WorkoutInfo.target_time -= "00:00:10"       
                    else:
                        Response({"error" : "feedback 반영 실패, 현재 최소"}, status=400)                      

            User_WorkoutInfo.save()

            return Response({
                        "code" : 200,
                        "message" : "feedback 반영 완료",
                    })
        except:
            return Response({"error" : "feedback 반영 실패"}, status=400)
