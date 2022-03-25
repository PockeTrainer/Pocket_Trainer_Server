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

        # 유저정보(체중, 키), 체력평가 여부 확인
        weight = user.weight
        height = user.height
        
        if not weight or not height:
            return Response({"error":"mainpage정보 호출 실패, 유저 정보 필요"}, status=400)

        if UserTest_Result == None:
            return Response({"error":"mainpage정보(운동) 호출 실패, 체력평가 결과 필요"}, status=400) 

        #오늘의 루틴 기록
        today = datetime.datetime.now().date()
        DayHistory_Workout_q = DayHistoryWorkout.objects.filter(user_id=user, create_date=today)
        DayHistoryWorkout_Serializer = DayHistorySerializer(DayHistory_Workout_q, many=True)

        if len(DayHistory_Workout_q) == 0:
            return Response({"error":"mainpage정보 호출 실패, 오늘의 루틴 생성 필요"}, status=400)

        #운동 성취도(clear 운동 비율)
        cleared_workout = DayHistoryWorkout.objects.filter(user_id=user, create_date=today, is_clear=True)
        percentage = int(len(cleared_workout) / len(DayHistory_Workout_q) * 100)

        #오늘 먹은 음식 기록
        DayHistoryDiet_q = DayHistoryDiet.objects.filter(user_id=user, create_date=today)
        DayHistoryDiet_Serializer = DayHistoryDietSerializer(DayHistoryDiet_q, many=True)

        #오늘 섭취해야 하는 칼로리 (목표 칼로리)
        DayHistory_UserInfo= DayHistoryUserInfo.objects.get(user_id=user, create_date=today)
        target_kcal = DayHistory_UserInfo.target_kcal

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
            "todayRoutine" : DayHistoryWorkout_Serializer.data,
            "clear_workout_percentage" : percentage,
            "day_history_diet" : DayHistoryDiet_Serializer.data,
            "target_kcal" : target_kcal,
            "today_kcal" : today_kcal,
            "diff_kcal" : diff_kcal,
            "nutrient_graph" : {
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

#월 기록 호출
class MonthHistoryView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, year_month, user_id):
        #try:
        user = User.objects.get(id=user_id)

        #섭취한 탄,단,지 list (6일)
        bmi_list = []        
        is_clear_list = []
        
        for i in range(1, 31+1):
            year_month_day = year_month+'-'+str(i)
            format = '%Y-%m-%d'
            #해당월 있는 일수 까지만 
            try:
                target_day = datetime.datetime.strptime(year_month_day, format)
            except:
                break

            target_DayHistoryUserInfo = DayHistoryUserInfo.objects.filter(user_id=user, create_date=target_day)
            
            #해당일 기록 없다면 bmi_list에 -1 추가
            if len(target_DayHistoryUserInfo) == 0 or target_DayHistoryUserInfo[0].bmi == None:
                bmi_list.append(-1)
            else:    
                bmi_list.append(target_DayHistoryUserInfo[0].bmi)
            
            target_day_workout = DayHistoryWorkout.objects.filter(user_id=user, create_date=target_day)
            cleared_workout = DayHistoryWorkout.objects.filter(user_id=user, create_date=target_day, is_clear=True)
            # 운동루틴 생성하지 않은 날 -1 추가
            if len(target_day_workout) == 0:
                is_clear_list.append(-1)
                continue
            percentage = len(cleared_workout) / len(target_day_workout)
            #운동 clear한 날(50%이상 수행)은 True, 아닌 날은 False 추가
            if percentage >= 0.5:
                is_clear_list.append(True)
            else:
                is_clear_list.append(False)


        return Response({
                "code" : "200",
                "message" : "월 기록 호출 완료",
                "bmi_list" : bmi_list,        
                "is_clear_list" : is_clear_list
            })


#일 기록 호출
class DayHistoryView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, date, user_id):
        #try:
        user = User.objects.get(id=user_id)

        # 유저정보(체중, 키), 체력평가 여부 확인
        weight = user.weight
        height = user.height
        
        if not weight or not height or user.activation_level not in [0,1,2,3,4] or user.target_weight not in [0,1,2]:
            return Response({"error":"mainpage정보 호출 실패, 유저 정보 필요"}, status=400)

        DayHistory_UserInfo = DayHistoryUserInfo.objects.filter(user_id=user, create_date = date)

        #해당일 유저 정보 없거나, 무게 정보 없다면 무게 표시 x
        if len(DayHistory_UserInfo)==0 or DayHistory_UserInfo[0].weight == None:
            day_weight = None
            day_bmi = None
        else:    
            day_weight = DayHistory_UserInfo[0].weight
            day_bmi = DayHistory_UserInfo[0].bmi

        #해당일 운동 기록 기록
        DayHistory_Workout_q = DayHistoryWorkout.objects.filter(user_id=user, create_date=date)
        DayHistoryWorkout_Serializer = DayHistorySerializer(DayHistory_Workout_q, many=True)

        #해당일 먹은 음식 기록
        DayHistoryDiet_q = DayHistoryDiet.objects.filter(user_id=user, create_date=date)
        DayHistoryDiet_Serializer = DayHistoryDietSerializer(DayHistoryDiet_q, many=True)

        #해달일 섭취해야 하는 칼로리 (목표 칼로리), 탄단지 g
        DayHistory_UserInfo, created = DayHistoryUserInfo.objects.update_or_create(user_id=user, create_date=date)

        #해당일 목표 칼로리 설정 되어 있지 않았다면 목표칼로리 생성
        if created:
            format = '%Y-%m-%d'
            date_ = datetime.datetime.strptime(date, format)
            age = date_.year - user.birth.year
            #기초 대사량
            basic_kcal = 0
            if ('man' in user.gender):
                basic_kcal = 66 + (13.7*user.weight) + (5*user.height) - (6.8*age)
            elif ('woman' in user.gender):
                basic_kcal = 655 + (9.6*user.weight) + (1.7*user.height) - (4.7*age)
            
            #유지 칼로리
            w1_list = [1.2, 1.375, 1.55, 1.725, 1.9]  #가중치
            maintain_kcal = basic_kcal * w1_list[user.activation_level]
            
            #목표 칼로리
            w2_list = [0.8, 1.0, 1.2]
            target_kcal = maintain_kcal * w2_list[user.target_weight]
            
            DayHistory_UserInfo.target_kcal = int(target_kcal)
            DayHistory_UserInfo.save()

        target_kcal = DayHistory_UserInfo.target_kcal
        target_carbohydrate = (target_kcal // 10 * 5) // 4
        target_protein = (target_kcal // 10 * 3) // 4
        target_province = (target_kcal // 10 * 2) // 9

        #해당일 섭취한 총 칼로리, 탄단지g
        total_kcal = 0
        carbohydrate = 0
        protein = 0
        province = 0
        for i in range(len(DayHistoryDiet_q)):
            total_kcal += DayHistoryDiet_q[i].food_kcal
            carbohydrate += DayHistoryDiet_q[i].carbohydrate
            protein += DayHistoryDiet_q[i].protein
            province += DayHistoryDiet_q[i].province

        return Response({
                "code" : "200",
                "message" : "일 기록 호출 완료",
                "day_weight" : day_weight,
                "day_bmi" : day_bmi,
                "day_history_workout" : DayHistoryWorkout_Serializer.data,
                "day_history_diet" : DayHistoryDiet_Serializer.data,
                "nutrient" : {
                    "target_kcal" : target_kcal,
                    "target_carbohydrate" : target_carbohydrate,
                    "target_protein" : target_protein,
                    "target_province" : target_province,

                    "total_kcal" : total_kcal,
                    "carbohydrate" : carbohydrate,       
                    "protein" : protein,
                    "province" : province 
                }
            })
        #except:
        #     return Response({"error":"해당일 기록이 존재하지 않습니다."}, status=400)

