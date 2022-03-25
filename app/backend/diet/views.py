from tkinter import W
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User, DayHistoryUserInfo
from .models import DayHistoryDiet

#from .models import dayHistoryUserInfo, dayHistoryWorkout, workoutInfo
from accounts.serializers import UserSerializer
from .serializers import DayHistoryDietSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

import datetime
# Create your views here.

class CreateTargetKcalView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def post(self, request, user_id):
        today = datetime.datetime.now().date()

        user = User.objects.get(id=user_id)
        
        #유저정보(체중, 키) 입력 여부 확인
        weight = user.weight
        height = user.height
        if not weight or not height or user.activation_level not in [0,1,2,3,4] or user.target_weight not in [0,1,2]:
            return Response({"error":"mainpage정보 호출 실패, 유저 정보 필요"}, status=400) 

        DayHistory_UserInfo, created = DayHistoryUserInfo.objects.update_or_create(user_id=user, create_date=today)

        #DayHistory_UserInfo 생성했을 경우
        if created:
            bmi = round(float(user.weight) / ((height/100)*(height/100)), 1)
            # DayHistory_UserInfo.weight = user.weight
            # DayHistory_UserInfo.bmi = bmi
            age = today.year - user.birth.year
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

        return Response({
                "code" : "200",
                "message" : "목표 kcal 설정 완료"
            })

#기록 호출
class DietView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, date, user_id):
        #try:
        #해당일 먹은 음식 기록
        user = User.objects.get(id=user_id)
        DayHistoryDiet_q = DayHistoryDiet.objects.filter(user_id=user, create_date = date)
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
                "message" : "식단 호출 완료",
                "day_history_diet" : DayHistoryDiet_Serializer.data,

                "target_kcal" : target_kcal,
                "target_carbohydrate" : target_carbohydrate,
                "target_protein" : target_protein,
                "target_province" : target_province,

                "total_kcal" : total_kcal,
                "carbohydrate" : carbohydrate,       
                "protein" : protein,
                "province" : province 
            })

    def post(self, request, date, user_id):
                #try:
        user = User.objects.get(id=user_id)
        DayHistory_Diet = DayHistoryDiet.objects.create(user_id=user, create_date = date)
        DayHistory_Diet.time = request.data['time']
        DayHistory_Diet.food_name = request.data['food_name']
        DayHistory_Diet.food_g = request.data['food_g']
        DayHistory_Diet.food_kcal = request.data['food_kcal']
        DayHistory_Diet.carbohydrate = request.data['carbohydrate']
        DayHistory_Diet.protein = request.data['protein']
        DayHistory_Diet.province = request.data['province']
        DayHistory_Diet.save()

        return Response({
                "code" : "200",
                "message" : "먹은 음식 추가 완료"
            })