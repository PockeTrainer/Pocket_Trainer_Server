from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, DayHistoryUserInfo
from .serializers import UserSerializer
from .OAuthInfo import NAVER_REST_API_KEY, NAVER_SECRET, KAKAO_REST_API_KEY

from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

from datetime import datetime
import requests
import urllib.request
import json

class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        #user를 create 해당 값 넣은 다음 다음 저장
        users = User.objects.all()
        if users.filter(username = request.data['id']).exists() :
            return Response({"error":"이미 존재하는 아이디입니다"}, status=409)
        try :
            user = User.objects.create_user(
                    username=request.data['id'], 
                    password=request.data['password'],
                    name=request.data['name'],
                    gender=request.data['gender'],
                    email=request.data['email'],
                    birth=request.data['birth'],
                )

            user.save()
            
            token = Token.objects.create(user=user)
            return Response({
                "code" : "200",
                "message": "회원가입완료", 
                "token": token.key
            })
        except :
            return Response({"error":"모두 입력해주세요"}, status=409)

class LogInView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = authenticate(username=request.data['id'], password=request.data['password'])
        if user is not None:
            q = User.objects.get(username=request.data['id'])
            serializer = UserSerializer(q)

            token = Token.objects.get(user=user)
            return Response({
                "code" : 200,
                "message": "로그인완료",
                "User": serializer.data,
                "Token": token.key
            })
        else:
            return Response({"error":"존재하지 않는 ID 이거나 PassWord입니다"}, status=409)

class NaverLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, code, state):
        naver_token_api = 'https://nid.naver.com/oauth2.0/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': NAVER_REST_API_KEY,
            'client_secret': NAVER_SECRET,
            'code': code,
            'state': state
        }

        token_response = requests.post(naver_token_api, data=data)

        access_token = token_response.json().get('access_token')

        header = "Bearer " + access_token        # Bearer 다음에 공백 추가
        url = "https://openapi.naver.com/v1/nid/me"
        request = urllib.request.Request(url)
        request.add_header("Authorization", header)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)

        user_info = json.loads(response_body.decode('utf-8'))
        user_id = user_info['response']['id']

        #소셜로그인 진행
        users = User.objects.all()

        #처음 로그인하는 유저: 회원가입 -> 로그인 
        #이미 로그인한 이력 있는 유저: 로그인
        #회원가입
        mw = ''
        if user_info['response']['gender'] == 'M':
            mw = 'man'
        elif user_info['response']['gender'] == 'F':
            mw = 'woman'
        if not users.filter(username = user_id).exists() :
            user = User.objects.create_user(
                    username=user_info['response']['id'], 
                    password=user_info['response']['id'],
                    name=user_info['response']['name'],
                    gender=mw,
                    email=user_info['response']['email'],
                    birth=user_info['response']['birthyear']+'-'+user_info['response']['birthday'],
                )
            user.save()
            
            token = Token.objects.create(user=user)
            print('회원가입 완료')

        #로그인
        user = authenticate(username=user_id, password=user_id)
        if user is not None:
            q = User.objects.get(username=user_id)
            serializer = UserSerializer(q)

            token = Token.objects.get(user=user)
            return Response({
                "code" : 200,
                "message": "로그인완료",
                "User": serializer.data,
                "Token": token.key
            })

        return Response({"error":"에러발생"}, status=400)


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, code):

        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_REST_API_KEY,
            'redirection_uri': 'http://localhost:8000/user/kakao/login',
            'code': code
        }
        token_response = requests.post(kakao_token_api, data=data)

        access_token = token_response.json().get('access_token')
        header = "Bearer " + access_token # Bearer 다음에 공백 추가
        url = "https://kapi.kakao.com/v2/user/me"
        request = urllib.request.Request(url)
        request.add_header("Authorization", header)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)

        user_info = json.loads(response_body.decode('utf-8'))
        user_id = user_info['id']

        #소셜로그인 진행
        users = User.objects.all()

        #처음 로그인하는 유저: 가지고 있는 정보 채워서 회원가입 창으로 이동 
        if not users.filter(username = user_id).exists() :
            id = user_id
            password = user_id
            name = user_info['kakao_account']['profile']['nickname']
            email = user_info['kakao_account']['email']     
            mw = ''
            if user_info['kakao_account']['gender'] == 'male':
                mw = 'man'
            elif user_info['kakao_account']['gender'] == 'female':
                mw = 'woman'
            return Response({
                "code" : 200,
                "message": "회원정보 불러오기 완료, 회원가입 창 이동",
                "id" : id,
                "password" : password,
                "name" : name,
                "email" : email,
                "gender" : mw
            })
        #이미 로그인한 이력 있는 유저: 로그인
        else: 
            user = authenticate(username=user_id, password=user_id)
            if user is not None:
                q = User.objects.get(username=user_id)
                serializer = UserSerializer(q)

                token = Token.objects.get(user=user)
                return Response({
                    "code" : 200,
                    "message": "로그인완료",
                    "User": serializer.data,
                    "Token": token.key
                })

        return Response({"error":"에러발생"}, status=400)


class BeginningUserInfoView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.height = float(request.data['height'])
            user.weight = float(request.data['weight'])
            user.activation_level = int(request.data['activation_level'])
            user.target_weight = int(request.data['target_weight'])
            user.save()

            today = datetime.now().date()
            DayHistory_UserInfo, created = DayHistoryUserInfo.objects.update_or_create(user_id=user, create_date=today)
            #DayHistory_UserInfo 생성했을 경우
            if created:
                bmi = round(float(request.data['weight']) / ((float(request.data['height'])/100)*(float(request.data['height'])/100)), 1)
                DayHistory_UserInfo.weight = user.weight
                DayHistory_UserInfo.bmi = bmi
                age = today.year - user.birth.year
                #기초 대사량
                basic_kcal = 0
                if ('man' in user.gender):
                    basic_kcal = 66 + (13.7*float(user.weight)) + (5*float(user.height)) - (6.8*age)
                elif ('woman' in user.gender):
                    basic_kcal = 655 + (9.6*float(user.weight)) + (1.7*float(user.height)) - (4.7*age)
                #유지 칼로리
                w1_list = [1.2, 1.375, 1.55, 1.725, 1.9]  #가중치
                maintain_kcal = basic_kcal * w1_list[int(user.activation_level)]
                #목표 칼로리
                w2_list = [0.8, 1.0, 1.2]
                target_kcal = maintain_kcal * w2_list[int(user.target_weight)]
                DayHistory_UserInfo.target_kcal = int(target_kcal)
                DayHistory_UserInfo.save()


            return Response({
                    "code" : 200,
                    "message": "유저 초기 키, 몸무게, 활동량, 목표체중 설정 완료",
                })
        except:
            return Response({"error":"모두 입력해주세요"}, status=409)


class DayUserInfoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, date, user_id):
        try:
            user = User.objects.get(id=user_id)

            #유저정보(체중, 키, 활동량, 감량증량) 입력 여부 확인
            weight = user.weight
            height = user.height
            if not weight or not height or user.activation_level not in [0,1,2,3,4] or user.target_weight not in [0,1,2]:
                return Response({"error":"mainpage정보 호출 실패, 유저 정보 필요"}, status=400)

            user.weight = request.data['weight']    #유저 weight 변경

            bmi = round(float(request.data['weight']) / ((height/100)*(height/100)), 1)
            DayHistory_UserInfo, created = DayHistoryUserInfo.objects.update_or_create(user_id=user, create_date=date)
            DayHistory_UserInfo.weight = request.data['weight']
            DayHistory_UserInfo.bmi = bmi

            #해당일 목표 칼로리 설정 되어 있지 않았다면 생성
            format = '%Y-%m-%d'
            date_ = datetime.strptime(date, format)
            age = date_.year - user.birth.year

            #기초 대사량
            basic_kcal = 0
            if ('man' in user.gender):
                basic_kcal = 66 + (13.7*float(request.data['weight'])) + (5*height) - (6.8*age)
            elif ('woman' in user.gender):
                basic_kcal = 655 + (9.6*float(request.data['weight'])) + (1.7*height) - (4.7*age)
            
            #유지 칼로리
            w1_list = [1.2, 1.375, 1.55, 1.725, 1.9]  #가중치
            maintain_kcal = basic_kcal * w1_list[user.activation_level]
            
            #목표 칼로리
            w2_list = [0.8, 1.0, 1.2]
            target_kcal = maintain_kcal * w2_list[user.target_weight]
            
            DayHistory_UserInfo.target_kcal = int(target_kcal)

            DayHistory_UserInfo.save()
            user.save()

            return Response({
                    "code" : 200,
                    "message": "몸무게, BMI 정보 저장 완료",
                })
        except:
            return Response({"error":"모두 입력해주세요"}, status=409)
