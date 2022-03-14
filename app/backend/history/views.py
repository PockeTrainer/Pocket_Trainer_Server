from django.shortcuts import render
#generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User, DayHistoryUserInfo, UserTestResult
from workout.models import DayHistoryWorkout
from diet.models import DayHistoryDiet
#from .models import dayHistoryUserInfo, dayHistoryWorkout, workoutInfo
from accounts.serializers import UserSerializer
from workout.serializers import DayHistorySerializer
from diet.serializers import DayHistoryDietSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

import datetime

#mainpage 정보 호출
class MainPageInfoView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        #try:

        user = User.objects.get(id=user_id)

        #최근 운동 평가 기록
        UserTest_Result = UserTestResult.objects.filter(user_id=user).last()
        if UserTest_Result == None:
            return Response({"error":"mainpage정보(운동) 호출 실패, 체력평가 결과 필요"}, status=400) 

        # 유저정보(체중, 키), 체력평가 여부 확인
        # modal_seq - 0: 둘다x, 1:유저정보o, 2:유저정보o, 체력평가o
        weight = user.weight
        height = user.height
        
        modal_seq = 0
        if weight and height:
            modal_seq = 1
        if UserTest_Result != None:
            modal_seq = 2

        #오늘의 루틴 기록
        today = datetime.datetime.now().date()
        DayHistory_Workout_q = DayHistoryWorkout.objects.filter(user_id=user, create_date=today)
        DayHistoryWorkout_Serializer = DayHistorySerializer(DayHistory_Workout_q, many=True)

        #운동 성취도(clear 운동 비율)
        cleared_workout = DayHistoryWorkout.objects.filter(user_id=user, create_date=today, is_clear=True)
        percentage = int(len(cleared_workout) / len(DayHistory_Workout_q) * 100)

        #오늘 먹은 음식 기록
        DayHistoryDiet_q = DayHistoryDiet.objects.filter(user_id=user, create_date=today)
        DayHistoryDiet_Serializer = DayHistoryDietSerializer(DayHistoryDiet_q, many=True)
        
        #오늘 섭취한 총 칼로리
        today_kcal = 0
        for i in range(len(DayHistoryDiet_q)):
            today_kcal += DayHistoryDiet_q[i].food_kcal

        #어제 섭취한 총 칼로리
        yesterday = today - datetime.timedelta(1)
        yesterday_DayHistoryDiet = DayHistoryDiet.objects.filter(user_id=user, create_date=yesterday)

        yesterday_kcal = 0
        for i in range(len(yesterday_DayHistoryDiet)):
            yesterday_kcal += yesterday_DayHistoryDiet[i].food_kcal

        #오늘 - 어제 칼로리
        diff_kcal = today_kcal - yesterday_kcal

        #섭취한 탄,단,지 list (6일)
        carbohydrate_list = []        
        protein_list = []
        province_list = []
        
        for i in range(6-1, -1, -1):
            target_day = today - datetime.timedelta(i)
            target_DayHistoryDiet = DayHistoryDiet.objects.filter(user_id=user, create_date=target_day)
            
            target_day_carbohydrate, target_day_protein, target_day_province = 0, 0, 0
            for j in range(len(target_DayHistoryDiet)): 
                target_day_carbohydrate += target_DayHistoryDiet[j].carbohydrate
                target_day_protein += target_DayHistoryDiet[j].protein
                target_day_province += target_DayHistoryDiet[j].province
            
            carbohydrate_list.append(target_day_carbohydrate)
            protein_list.append(target_day_protein)
            province_list.append(target_day_province)
            
        # upperbody_strength = UserTest_Result.upperbody_strength
        # stomach_strength = UserTest_Result.stomach_strength
        # lowerbody_strength = UserTest_Result.lowerbody_strength
        # date = UserTest_Result.create_date

        return Response({
            "code" : 200,
            "message" : "mainpage 정보 확인 완료",
            "modal_seq" : modal_seq,
            "todayRoutine" : DayHistoryWorkout_Serializer.data,
            "clear_workout_percentage" : percentage,
            "day_history_diet" : DayHistoryDiet_Serializer.data,
            "today_kcal" : today_kcal,
            "diff_kcal" : diff_kcal,
            "diet_graph" : {
                "carbohydrate_list" : carbohydrate_list,        
                "protein_list" : protein_list,
                "province_list" : province_list
            }     
            # "testResult" : {
            #     "upperbody_strength" : upperbody_strength,   
            #     "stomach_strength" : stomach_strength,        
            #     "lowerbody_strength" : lowerbody_strength,
            #     "date" : date   
            # },
                #"changeGraph" : {
                #    "start_month" : start_month,    
                #    "count" : count                 
                #}

                #"today_kcal" : today_kcal
                # "dietGraph" : {
                #     "carbohydrate" : carbohydrate,    ]
                #     "protein", protein,                80]
                #     "province", province              
                # }
                
        })
        #except:
        #    return Response({"error":"mainpage 정보 호출 실패."}, status=400)


#기록 호출
class DayHistoryView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, date, user_id):
        #try:
        user = User.objects.get(id=user_id)
        DayHistory_UserInfo = DayHistoryUserInfo.objects.filter(user_id=user, create_date = date)

        if len(DayHistory_UserInfo) == 0:
            day_weight = None
            day_bmi = None
        else:    
            day_weight = DayHistory_UserInfo[0].weight
            day_bmi = DayHistory_UserInfo[0].bmi

        #오늘의 루틴 기록
        DayHistory_Workout_q = DayHistoryWorkout.objects.filter(user_id=user, create_date=date)
        DayHistoryWorkout_Serializer = DayHistorySerializer(DayHistory_Workout_q, many=True)

        #오늘 먹은 음식 기록
        DayHistoryDiet_q = DayHistoryDiet.objects.filter(user_id=user, create_date=date)
        DayHistoryDiet_Serializer = DayHistoryDietSerializer(DayHistoryDiet_q, many=True)

        return Response({
                "code" : "200",
                "message" : "기록 호출 완료",
                "day_weight" : day_weight,
                "day_bmi" : day_bmi,
                "day_history_workout" : DayHistoryWorkout_Serializer.data,
                "day_history_diet" : DayHistoryDiet_Serializer.data
            })
        #except:
        #     return Response({"error":"해당일 기록이 존재하지 않습니다."}, status=400)

