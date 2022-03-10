from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from .models import DayHistoryDiet

#from .models import dayHistoryUserInfo, dayHistoryWorkout, workoutInfo
from accounts.serializers import UserSerializer
from .serializers import DayHistoryDietSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

import datetime
# Create your views here.

#기록 호출
class DietView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request, date, user_id):
        #try:
        user = User.objects.get(id=user_id)
        DayHistory_Diet_q = DayHistoryDiet.objects.filter(user_id=user, create_date = date)
        DayHistoryDiet_Serializer = DayHistoryDietSerializer(DayHistory_Diet_q, many=True)

        return Response({
                "code" : "200",
                "message" : "식단 호출 완료",
                "day_history_diet" : DayHistoryDiet_Serializer.data
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